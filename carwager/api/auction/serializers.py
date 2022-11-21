from rest_framework import serializers

from auction.models import Auction


class AuctionModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Auction
        fields = ["id", "win", "image", "description",
                  "price", "created_at", "date_start", "date_end", "status"]
        read_only_fields = ("id", "win", "image", "description",
                            "price", "created_at", "date_start", "date_end", "status")
