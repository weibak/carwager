import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import ValidationError

from auction.models import Auction


class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(f"🔗 Auction WebSocket connect attempt")

        self.auction_id = self.scope['url_route']['kwargs'].get('auction_id')
        print(f"   Auction ID: {self.auction_id}")

        # Get user
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            print("   ❌ User not authenticated, closing connection")
            await self.close(code=4001)  # Custom code for auth error
            return

        print(f"   👤 User: {self.user.username} (ID: {self.user.id})")

        try:
            # Get auction
            self.auction = await self.get_auction()

            print(f"   ✅ Auction ID: {self.auction.id}")

            self.room_group_name = f'auction_{self.auction.id}'
            print(f"   Room group name: {self.room_group_name}")

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            print("   ✅ Added to channel layer group")

            await self.accept()
            print("   ✅ WebSocket connection accepted")

            # Send current auction price
            await self.send(json.dumps({
                'type': 'auction_info',
                'current_price': str(self.auction.price),
                'message': f'Connected to auction {self.auction.id}',
                'auction_id': self.auction.id
            }))

        except Exception as e:
            print(f"   ❌ Error in connect: {e}")
            import traceback
            traceback.print_exc()
            await self.close(code=4000)  # Custom code for general error

    async def disconnect(self, close_code):
        print(f"🔌 Auction WebSocket disconnect, code: {close_code}")
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            print("   ✅ Removed from channel layer group")

    async def receive(self, text_data):
        print(f"📨 Received message from {self.user.username}")
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type', '')

            if message_type == 'bid':
                bid_amount = text_data_json.get('bid_amount', '').strip()

                if not bid_amount:
                    return

                # Process bid
                bid_result = await self.process_bid(bid_amount)

                if bid_result.get('success'):
                    # Send bid update to all connected clients
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'bid_update',
                            'bid_id': bid_result['bid_id'],
                            'user_id': self.user.id,
                            'user_username': self.user.username,
                            'bid_amount': bid_amount,
                            'new_price': str(bid_result['new_price']),
                            'timestamp': bid_result['timestamp'],
                        }
                    )
                else:
                    # Send error to this client only
                    await self.send(json.dumps({
                        'type': 'bid_error',
                        'message': bid_result['message']
                    }))

        except Exception as e:
            print(f"   ❌ Error in receive: {e}")

    async def bid_update(self, event):
        """Send bid update to all connected clients"""
        await self.send(text_data=json.dumps({
            'type': 'bid_update',
            'bid_id': event['bid_id'],
            'user_id': event['user_id'],
            'user_username': event['user_username'],
            'bid_amount': event['bid_amount'],
            'new_price': event['new_price'],
            'timestamp': event['timestamp'],
        }))

    async def price_update(self, event):
        """Send price update to all connected clients"""
        await self.send(text_data=json.dumps({
            'type': 'price_update',
            'new_price': event['new_price'],
            'auction_id': event['auction_id'],
        }))

    @database_sync_to_async
    def get_auction(self):
        from .models import Auction
        from django.core.exceptions import ObjectDoesNotExist

        try:
            auction = Auction.objects.get(id=self.auction_id)
            print(f"Found existing auction: {auction.id}")
        except ObjectDoesNotExist:
            print(f"Auction #{self.auction_id} not found")
            raise Exception(f"Auction #{self.auction_id} not found")

        return auction

    @database_sync_to_async
    def process_bid(self, bid_amount):
        from .bid_processor import process_bid_with_retry
        from django.utils import timezone
        from .models import Bid

        try:
            if self.auction.owner.id == self.user.id:
                return {
                    'success': False,
                    'message': "You can't bid on your auction"
                }

            # Use atomic bid processor with retry
            success, message, new_price, bid_id = process_bid_with_retry(
                auction_id=self.auction.id,
                user_id=self.user.id,
                bid_amount_str=bid_amount,
                max_retries=3
            )

            if success:
                # Get bid timestamp
                bid = Bid.objects.get(id=bid_id)
                
                # Refresh auction instance
                self.auction.refresh_from_db()
                
                return {
                    'success': True,
                    'bid_id': bid_id,
                    'new_price': new_price,
                    'timestamp': bid.created_at.isoformat()
                }
            else:
                return {
                    'success': False,
                    'message': message
                }

        except Exception as e:
            print(f"   ❌ Error processing bid: {e}")
            return {
                'success': False,
                'message': str(e)
            }
