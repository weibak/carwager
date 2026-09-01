import json
from logging import getLogger

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .bid_processor import process_bid_with_retry
from .models import Auction, Bid

logger = getLogger(__name__)


class AuctionConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.auction_id = None
        self.auction = None
        self.user = None
        self.room_group_name = None

    async def connect(self):
        self.auction_id = self.scope["url_route"]["kwargs"].get("auction_id")
        self.user = self.scope["user"]

        logger.debug(
            "WebSocket connection attempt: user=%s, auction_id=%s",
            self.user.username if self.user.is_authenticated else "anonymous",
            self.auction_id,
        )

        if not self.user.is_authenticated:
            logger.debug("Unauthenticated user. Closing connection.")
            await self.close(code=4001)
            return

        try:
            self.auction = await self.get_auction()

            self.room_group_name = f"auction_{self.auction.id}"

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name,
            )

            await self.accept()

            logger.debug(
                "WebSocket connected: user=%s, auction_id=%s",
                self.user.username,
                self.auction.id,
            )

            await self.send(
                text_data=json.dumps(
                    {
                        "type": "auction_info",
                        "current_price": str(self.auction.price),
                        "auction_id": self.auction.id,
                    }
                )
            )

        except Auction.DoesNotExist:
            logger.warning(
                "Auction not found: auction_id=%s",
                self.auction_id,
            )
            await self.close(code=4004)

        except Exception as e:
            logger.exception(
                f"Error during WebSocket connection: auction_id=%s. Info: {e}",
                self.auction_id,
            )
            await self.close(code=4000)

    async def disconnect(self, code):
        logger.debug(
            "WebSocket disconnected: user=%s, auction_id=%s, code=%s",
            self.user.username if self.user else "unknown",
            self.auction_id,
            code,
        )

        if self.room_group_name:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name,
            )

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is None:
            return

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send_error("Invalid JSON.")
            return

        message_type = data.get("type")

        if message_type == "bid":
            await self.handle_bid(data)
            return

        logger.warning(
            "Unknown WebSocket message type: %s",
            message_type,
        )

    async def handle_bid(self, data):
        bid_amount = str(data.get("bid_amount", "")).strip()

        if not bid_amount:
            await self.send_error("Bid amount is required.")
            return

        bid_result = await self.process_bid(bid_amount)

        if not bid_result["success"]:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "bid_error",
                        "message": bid_result["message"],
                    }
                )
            )
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "bid_update",
                "bid_id": bid_result["bid_id"],
                "user_id": self.user.id,
                "user_username": self.user.username,
                "bid_amount": bid_amount,
                "new_price": str(bid_result["new_price"]),
                "timestamp": bid_result["timestamp"],
            },
        )

    async def send_error(self, message):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "bid_error",
                    "message": message,
                }
            )
        )

    async def bid_update(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "bid_update",
                    "bid_id": event["bid_id"],
                    "user_id": event["user_id"],
                    "user_username": event["user_username"],
                    "bid_amount": event["bid_amount"],
                    "new_price": event["new_price"],
                    "timestamp": event["timestamp"],
                }
            )
        )

    async def price_update(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "price_update",
                    "new_price": event["new_price"],
                    "auction_id": event["auction_id"],
                }
            )
        )

    @database_sync_to_async
    def get_auction(self):
        return Auction.objects.get(id=self.auction_id)

    @database_sync_to_async
    def process_bid(self, bid_amount):
        if self.auction.owner_id == self.user.id:
            return {
                "success": False,
                "message": "You can't bid on your own auction.",
            }

        try:
            success, message, new_price, bid_id = process_bid_with_retry(
                auction_id=self.auction.id,
                user_id=self.user.id,
                bid_amount_str=bid_amount,
                max_retries=3,
            )

            if not success:
                return {
                    "success": False,
                    "message": message,
                }

            bid = Bid.objects.get(id=bid_id)

            return {
                "success": True,
                "bid_id": bid.id,
                "new_price": new_price,
                "timestamp": bid.created_at.isoformat(),
            }

        except Exception as e:
            logger.exception(
                f"Error processing bid: user_id=%s, auction_id=%s\n info: {e}",
                self.user.id,
                self.auction.id,
            )

            return {
                "success": False,
                "message": "An error occurred while processing the bid.",
            }
