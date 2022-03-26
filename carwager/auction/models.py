from django.conf import settings
from django.db import models
from showbill.models import ENGINE_TYPE, GEAR_BOX, DRIVE


STATUS_AUC = (
    ("go", "Auction going "),
    ("soon", "Soon"),
    ("stop", "Auction ended")

)


class CarMarkAuction(models.Model):
    car_mark = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.car_mark}"


class CarModelAuction(models.Model):
    car_mark = models.ForeignKey(
        CarMarkAuction, related_name="carmodelsauction", on_delete=models.CASCADE
    )
    car_model = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.car_mark} - {self.car_model}"


class CarAuction(models.Model):
    mark = models.ForeignKey(
        CarMarkAuction, related_name="carsauction", on_delete=models.CASCADE
    )
    model = models.ForeignKey(
        CarModelAuction, related_name="carsauction", on_delete=models.CASCADE
    )
    year = models.IntegerField(default=None)
    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="favorite_carsauction"
    )

    def __str__(self):
        return f"{self.mark.car_mark} - {self.model.car_model}"


class Auction(models.Model):
    car = models.ForeignKey(
        CarAuction, related_name="auctions", on_delete=models.CASCADE
    )
    engine_type = models.CharField(max_length=100, choices=ENGINE_TYPE, default="No type")
    engine_capacity = models.FloatField(default="No capacity")
    drive = models.CharField(max_length=100, choices=DRIVE, default="No type")
    gear_box = models.CharField(max_length=100, choices=GEAR_BOX, default="No type")
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    win = models.CharField(max_length=17, null=True, blank=True)
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

    def __str__(self):
        return f"{self.car.mark} - {self.car.model} - {self.car.year}"


class Winner(models.Model):
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, default=None
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None
    )


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



