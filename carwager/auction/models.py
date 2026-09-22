from django.conf import settings
from django.db import models

from api import users
from showbill.models import Car
from showbill.models import ENGINE_TYPE, GEAR_BOX, DRIVE

STATUS_AUC = (
    ("", ""),
    ("go", "Auction going"),
    ("soon", "Soon"),
    ("stop", "Auction ended")

)


class Auction(models.Model):
    car = models.ForeignKey(
        Car, related_name="auctions", on_delete=models.CASCADE
    )
    engine_type = models.CharField(max_length=100, choices=ENGINE_TYPE, default="No type")
    engine_capacity = models.DecimalField(decimal_places=1, max_digits=5, default="No capacity")
    drive = models.CharField(max_length=100, choices=DRIVE, default="No type")
    gear_box = models.CharField(max_length=100, choices=GEAR_BOX, default="No type")
    description = models.TextField(blank=True, default="")
    win = models.CharField(max_length=17, blank=True, default="")
    price = models.DecimalField(decimal_places=2, max_digits=15)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="auctions"
    )
    phone_number = models.CharField(max_length=13)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True,)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_AUC, default="stop")
    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="favorite_auctions"
    )

    @property
    def gallery(self):
        return [item.image for item in self.images.all()]

    def __str__(self):
        return f"{self.car.mark} - {self.car.model} - {self.car.year}"


class AuctionImage(models.Model):
    auction = models.ForeignKey(Auction, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="auction_photos/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Auction image for {self.auction_id}"


class Winner(models.Model):
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, default=None
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None
    )
    def __str__(self):
        return f"Winner: {self.user.id} for {self.auction_id}"

class Bid(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="bids", on_delete=models.CASCADE
    )
    auction = models.ForeignKey(
        Auction, related_name="bids", on_delete=models.CASCADE
    )
    bef_bid_price = models.DecimalField(decimal_places=2, max_digits=15, default=0)
    bid = models.DecimalField(decimal_places=2, max_digits=15)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.user} - {self.auction.car} - {self.bid}"
