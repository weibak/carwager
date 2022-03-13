from django.conf import settings
from django.db import models


CAR_MARK = (
    ("bmw", "BMW"),
    ("merc", "MERCEDES"),
    ("toyo", "TOYOTA"),
)


ENGINE_TYPE = (
    ("petr", "Petrol"),
    ("dies", "Diesel"),
    ("hyb", "Hybrid"),
    ("elec", "Electro"),
)


DRIVE = (
    ("fwd", "Front-wheel drive"),
    ("rwd", "Rear-wheel drive"),
    ("awd", "Automatic 4WD"),
    ("4wd", "Full-time 4WD"),
)


GEAR_BOX = (
    ("auto", "Automatic"),
    ("man", "Manual"),
)


class Car(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="car"
    )
    car_mark = models.CharField(max_length=100, choices=CAR_MARK, default="No mark")
    car_model = models.CharField(max_length=25, default="No model")
    engine_type = models.CharField(max_length=100, choices=ENGINE_TYPE, default="No type")
    engine_capacity = models.IntegerField(default="No capacity")
    drive = models.CharField(max_length=100, choices=DRIVE, default="No type")
    gear_box = models.CharField(max_length=100, choices=GEAR_BOX, default="No type")
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    win = models.CharField(max_length=17, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=15)
    price_usd = models.DecimalField(default=0, decimal_places=2, max_digits=15)

    def __str__(self):
        return f"{self.car_mark} - {self.price}"
