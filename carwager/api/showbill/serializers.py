from rest_framework import serializers

from showbill.models import Advert, Car, CarModel, CarMark


class MarkModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMark
        fields = ["car_mark"]


class ModelModelSerializer(serializers.ModelSerializer):
    mark = MarkModelSerializer(source="car_mark")

    class Meta:
        model = CarModel
        fields = ["mark", "car_model"]


class CarModelSerializer(serializers.ModelSerializer):
    mark = ModelModelSerializer
    car_model = ModelModelSerializer(source="model")

    class Meta:
        model = Car
        fields = ["year", "car_model"]


class AdvertModelSerializer(serializers.HyperlinkedModelSerializer):
    car_ = CarModelSerializer(source="car")

    class Meta:
        model = Advert
        fields = ["car_", "engine_type", "engine_capacity", "drive", "gear_box", "description", "win", "image",
                  "price", "price_usd", "phone_number", "created_at"]
