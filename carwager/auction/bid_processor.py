"""
Bid processor with atomic operations to prevent race conditions
"""
from decimal import Decimal
from django.db import transaction
from django.db.models import F
from .models import Auction, Bid


def process_bid_atomic(auction_id, user_id, bid_amount_str):
    """
    Process a bid with atomic operations to prevent race conditions.
    Returns: (success, message, new_price, bid_id)
    """
    try:
        bid_amount = Decimal(bid_amount_str)
        
        with transaction.atomic():
            # Select auction with FOR UPDATE lock to prevent concurrent modifications
            auction = Auction.objects.select_for_update().get(id=auction_id)
            # Check if auction is active
            if auction.status != 'go':
                return False, 'Auction is not active', None, None
            
            # Check if bid is valid (positive amount)
            if bid_amount <= 0:
                return False, 'Bid amount must be positive', None, None
            
            # Get current price before any updates
            current_price = auction.price
            
            # Check if there are any bids at the current price (race condition check)
            # This is atomic because we're in a transaction with SELECT FOR UPDATE
            existing_bids = Bid.objects.filter(
                auction=auction, 
                bef_bid_price=current_price
            ).exists()
            
            if existing_bids:
                return False, 'Ставка перебита! Кто-то уже сделал ставку по текущей цене. Обновите страницу и попробуйте снова.', None, None
            
            # Create the bid
            bid = Bid.objects.create(
                auction=auction,
                user_id=user_id,
                bid=bid_amount,
                bef_bid_price=current_price
            )
            
            # Update auction price atomically
            Auction.objects.filter(id=auction_id).update(price=F("price") + bid_amount)
            
            # Get the new price
            auction.refresh_from_db()
            new_price = auction.price
            
            return True, 'Ставка успешно принята!', str(new_price), bid.id
            
    except Auction.DoesNotExist:
        return False, 'Auction not found', None, None
    except Exception as e:
        return False, f'Error processing bid: {str(e)}', None, None


def process_bid_with_retry(auction_id, user_id, bid_amount_str, max_retries=3):
    """
    Process a bid with retry logic for concurrent bids.
    Returns: (success, message, new_price, bid_id)
    """
    for attempt in range(max_retries):
        success, message, new_price, bid_id = process_bid_atomic(
            auction_id, user_id, bid_amount_str
        )
        
        if success:
            return success, message, new_price, bid_id
        elif 'Ставка перебита' in message and attempt < max_retries - 1:
            # Retry if price changed (someone else placed a bid)
            continue
        else:
            # Other errors or max retries reached
            return success, message, new_price, bid_id
    
    return False, 'Не удалось сделать ставку после нескольких попыток. Кто-то активно делает ставки. Попробуйте позже.', None, None
