from rest_framework import serializers

from showbill.models import Advert, Car, CarModel


class ModelModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = "__all__"


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        car = Car
        fields = "__all__"


class AdvertModelSerializer(serializers.ModelSerializer):
    car = CarModelSerializer

    class Meta:
        model = Advert
        fields = ["id", "car", "engine_type", "engine_capacity", "drive", "gear_box", "description", "win", "image",
                  "price", "price_usd", "phone_number", "created_at"]
