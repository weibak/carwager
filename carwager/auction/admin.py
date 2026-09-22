from django.contrib import admin
from auction.models import Auction, Winner, Bid


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = (
        "car", "engine_type", "engine_capacity", "drive",
        "gear_box", "win",
        "price", "owner", "phone_number", "date_start", "date_end", "status",
    )
    fields = (
        "car", "engine_type", "engine_capacity", "drive",
        "gear_box", "description", "win",
        "price", "owner", "phone_number", "date_start", "date_end", "status",
    )
    search_fields = ("car", "engine_type", "gear_box", "status")
    readonly_fields = ("created_at",)
    list_filter = ["status"]


@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ("user", "auction")
    fields = ("user", "auction")


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ("user", "auction", "bid", "created_at")
    fields = ("user", "auction", "bef_bid_price", "bid")
    readonly_fields = ("created_at",)
