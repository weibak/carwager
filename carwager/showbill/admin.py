from django.contrib import admin

from showbill.models import Car, Advert, CarMark, CarModel


@admin.register(CarMark)
class CarMarkAdmin(admin.ModelAdmin):
    list_display = ("car_mark",)
    fields = ("car_mark",)
    search_fields = ("car_mark",)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("car_mark", "car_model")
    fields = ("car_mark", "car_model")
    search_fields = ("car_mark", "car_model")


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("mark", "model", "year")
    fields = ("mark", "model", "year")
    search_fields = ("mark", "model", "year")


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    list_display = (
        "car", "engine_type", "engine_capacity", "drive", "gear_box", "description", "image", "win", "price", "price_usd", "owner", "phone_number"
    )
    fields = ("car", "engine_type", "engine_capacity", "drive", "gear_box", "description", "image", "win", "price", "price_usd", "owner", "phone_number")
    search_fields = ("car", "engine_type", "gear_box")
    readonly_fields = ("created_at", )