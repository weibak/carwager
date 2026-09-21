from rest_framework import serializers

from auction.models import Auction


class AuctionModelSerializer(serializers.HyperlinkedModelSerializer):
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
        model = Auction
        fields = ["id", "car_id", "engine_type", "engine_capacity", "drive", "gear_box", "win", "image", "images",
                  "description", "price", "created_at", "date_start", "date_end", "status"]
