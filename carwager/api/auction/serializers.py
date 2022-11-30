from rest_framework import serializers

from auction.models import Auction


class AuctionModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Auction
        fields = ["id", "car_id", "engine_type", "engine_capacity", "drive", "gear_box", "win", "image", "description",
                  "price", "created_at", "date_start", "date_end", "status"]
