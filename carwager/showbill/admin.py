from django.contrib import admin
from django.utils.html import format_html
from showbill.models import Car, Advert, CarMark, CarModel, AdvertImage


@admin.register(CarMark)
class CarMarkAdmin(admin.ModelAdmin):
    list_display = ("car_mark",)
    fields = ("car_mark",)
    search_fields = ("car_mark",)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("car_mark", "car_model")
    fields = ("car_mark", "car_model")
    search_fields = ("car_mark__car_mark", "car_model")


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("mark", "model", "year")
    fields = ("mark", "model", "year")
    search_fields = ("mark__car_mark", "model__car_model", "year")


@admin.register(AdvertImage)
class AdvertImageAdmin(admin.ModelAdmin):
    list_display = ("advert", "image_preview", "created_at")
    list_filter = ("created_at", "advert")
    readonly_fields = ("image_preview", "created_at")

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="75" style="object-fit: cover; border-radius: 5px;" />',
                obj.image.url)
        return "No image"

    image_preview.short_description = "Preview"


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    list_display = (
        "car", "engine_type", "engine_capacity", "drive", "gear_box", "body", "description",
        "win", "price", "price_usd", "owner", "phone_number"
    )
    fields = ("car", "engine_type", "engine_capacity", "drive", "gear_box", "body", "description",
              "win", "price", "price_usd", "owner", "phone_number")
    search_fields = ("drive", "engine_type", "gear_box", "body")
    readonly_fields = ("created_at",)

    # Добавляем inline для отображения изображений прямо в админке объявления
    class AdvertImageInline(admin.TabularInline):
        model = AdvertImage
        extra = 1
        readonly_fields = ("image_preview",)

        def image_preview(self, obj):
            if obj.image:
                return format_html(
                    '<img src="{}" width="100" height="75" style="object-fit: cover; border-radius: 5px;" />',
                    obj.image.url)
            return "No image"

        image_preview.short_description = "Preview"

    inlines = [AdvertImageInline]
