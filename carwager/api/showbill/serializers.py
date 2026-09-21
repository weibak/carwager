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
    image = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_image(self, obj):
        if not obj.gallery:
            return None
        request = self.context.get("request")
        image = obj.gallery[0]
        return request.build_absolute_uri(image.url) if request else image.url

    def get_images(self, obj):
        request = self.context.get("request")
        return [request.build_absolute_uri(image.url) if request else image.url for image in obj.gallery]

    class Meta:
        model = Advert
        fields = ["car_", "engine_type", "engine_capacity", "drive", "gear_box", "description", "win", "image",
                  "images", "price", "price_usd", "phone_number", "created_at"]
