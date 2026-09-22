import datetime
import random

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.utils import timezone

from auction.models import Auction
from showbill.models import Car, CarModel, CarMark


@pytest.mark.django_db
class TestAuctionsAPI:
    def test_auctions_view(self):
        client = Client()

        user = User.objects.create(
            username="test", email="test@test.com", password="testtest"
        )

        mark = CarMark.objects.create(car_mark="test")
        model = CarModel.objects.create(car_mark=mark, car_model="test")
        car = Car.objects.create(mark=mark, model=model, year=random.randint(1800, 2022))
        Auction.objects.create(car=car, engine_type="Test", engine_capacity=random.randint(1, 10),
                               drive="No type", gear_box="No type", description="Test",
                               price=random.randrange(9999999999999), owner=user,
                               phone_number=random.randrange(9999999), date_start=timezone.now(),
                               date_end=timezone.now() + datetime.timedelta(days=1),
                               )

        client.force_login(user)

        response = client.get("/api/auctions/")
        assert response.status_code == 200
