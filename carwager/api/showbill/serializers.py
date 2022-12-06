from rest_framework import serializers

from showbill.models import Advert, Car, CarModel, CarMark


class MarkModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMark
        fields = ["id"]


class ModelModelSerializer(serializers.ModelSerializer):
    mark = MarkModelSerializer(source="*")

    class Meta:
        model = CarModel
        fields = ["mark", "id"]


class CarModelSerializer(serializers.ModelSerializer):
    car_model = ModelModelSerializer(source='*')

    class Meta:
        model = Car
        fields = ["id", "car_model", "year"]


class AdvertModelSerializer(serializers.HyperlinkedModelSerializer):
    car = CarModelSerializer(source='*')

    class Meta:
        model = Advert
        fields = ["id", "car", "engine_type", "engine_capacity", "drive", "gear_box", "description", "win", "image",
                  "price", "price_usd", "phone_number", "created_at"]
