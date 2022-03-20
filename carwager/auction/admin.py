from django.contrib import admin
from auction.models import CarAuction, Auction, CarMarkAuction, CarModelAuction


@admin.register(CarMarkAuction)
class CarMarkAuctionAdmin(admin.ModelAdmin):
    list_display = ("car_mark",)
    fields = ("car_mark",)
    search_fields = ("car_mark",)


@admin.register(CarModelAuction)
class CarModelAuctionAdmin(admin.ModelAdmin):
    list_display = ("car_mark", "car_model")
    fields = ("car_mark", "car_model")
    search_fields = ("car_mark", "car_model")


@admin.register(CarAuction)
class CarAuctionAdmin(admin.ModelAdmin):
    list_display = ("mark", "model", "year")
    fields = ("mark", "model", "year")
    search_fields = ("mark", "model", "year")


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = (
        "car", "engine_type", "engine_capacity", "drive",
        "gear_box", "description", "image", "win",
        "price", "price_usd", "owner", "phone_number", "date_start", "date_end", "status"
    )
    fields = (
        "car", "engine_type", "engine_capacity", "drive",
        "gear_box", "description", "image", "win",
        "price", "price_usd", "owner", "phone_number", "date_start", "date_end", "status"
    )
    search_fields = ("car", "engine_type", "gear_box", "status")
    readonly_fields = ("created_at",)
