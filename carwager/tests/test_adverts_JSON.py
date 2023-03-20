import pytest
import requests
import logging
from django.test import Client

logger = logging.getLogger(__name__)


@pytest.mark.django_db
class TestAdvertJSON:
    def test_advert_json(self):
        client = Client()

        query_set = requests.get("http://127.0.0.1:8000/api/adverts/")
        json = query_set.json()
        mark = []
        model = []
        year = []
        engine_type = []
        engine_capacity = []
        drive = []
        gear_box = []
        description = []
        image = []
        win = []
        price = []
        price_usd = []
        phone_number = []
        for car in json["results"]:
            mark.append(car['car_']['car_model']['mark']['car_mark'])
            model.append(car['car_']['car_model']['car_model'])
            year.append(car['car_']['year'])
            engine_type.append(car['engine_type'])
            engine_capacity.append(car['engine_capacity'])
            drive.append(car['drive'])
            gear_box.append(car['gear_box'])
            description.append(car['description'])
            image.append(car['image'])
            win.append(car['win'])
            price.append(car['price'])
            price_usd.append(car['price_usd'])
            phone_number.append(car['phone_number'])

        if (mark, model, year, engine_type, engine_capacity, drive, gear_box, description, image, win, price, price_usd,
                phone_number) is not None:
            pass
        else:
            raise Exception("Sorry, mark is not valid")

        response = client.get("/api/adverts/")
        assert response.status_code == 200
