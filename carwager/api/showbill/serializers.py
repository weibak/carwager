from rest_framework import serializers

from showbill.models import Advert


class AdvertModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Advert
        fields = ["id", "car_id", "engine_type", "engine_capacity", "drive", "gear_box", "description", "win", "image",
                  "price", "price_usd", "phone_number", "created_at"]
