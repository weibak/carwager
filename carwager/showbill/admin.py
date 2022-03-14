from django.contrib import admin

from showbill.models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("mark", "model", "year")
    fields = ("mark", "model", "year")
    search_fields = ("mark", "model", "year")
