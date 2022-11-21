from rest_framework import serializers

from showbill.models import Advert


class AdvertModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Advert
        fields = ["id", "win", "image", "description",
                  "price", "price_usd", "created_at"]
        read_only_fields = ("id", "win", "image", "description",
                            "price", "price_usd", "created_at")
