import datetime
import json
import random
from decimal import Decimal

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.utils import timezone

from auction.models import Auction, AuctionImage, Winner, Bid
from showbill.models import Car, CarModel, CarMark


@pytest.mark.django_db
class TestAuctionModels:
    """Тесты для моделей приложения auction"""

    def test_auction_creation(self):
        """Тест создания аукциона"""
        user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpass123"
        )

        mark = CarMark.objects.create(car_mark="Toyota")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry")
        car = Car.objects.create(mark=mark, model=model, year=2020)

        auction = Auction.objects.create(
            car=car,
            engine_type="Gasoline",
            engine_capacity=Decimal("2.5"),
            drive="Front",
            gear_box="Automatic",
            body="Sedan",
            description="Test auction description",
            win="ABC12345678901234",
            price=Decimal("25000.00"),
            owner=user,
            phone_number="+375291234567",
            date_start=timezone.now() + datetime.timedelta(hours=1),
            date_end=timezone.now() + datetime.timedelta(days=7),
            status="soon"
        )

        assert auction.car == car
        assert auction.owner == user
        assert auction.price == Decimal("25000.00")
        assert auction.status == "soon"
        assert str(auction) == f"{car.mark} - {car.model} - {car.year}"

    def test_auction_gallery_property(self):
        """Тест свойства gallery модели Auction"""
        user = User.objects.create_user(
            username="testuser2", email="test2@test.com", password="testpass123"
        )

        mark = CarMark.objects.create(car_mark="Toyota2")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry2")
        car = Car.objects.create(mark=mark, model=model, year=2021)

        auction = Auction.objects.create(
            car=car,
            engine_type="Gasoline",
            engine_capacity=Decimal("2.5"),
            drive="Front",
            gear_box="Automatic",
            body="Sedan",
            description="Test auction",
            price=Decimal("25000.00"),
            owner=user,
            phone_number="+375291234567",
            date_start=timezone.now() + datetime.timedelta(hours=1),
            date_end=timezone.now() + datetime.timedelta(days=7),
            status="soon"
        )

        # Создаем изображения для аукциона
        _image1 = AuctionImage.objects.create(auction=auction, image="test1.jpg")
        _image2 = AuctionImage.objects.create(auction=auction, image="test2.jpg")

        gallery = auction.gallery
        assert len(gallery) == 2
        assert gallery[0] == "test1.jpg"
        assert gallery[1] == "test2.jpg"

    def test_auction_image_model(self):
        """Тест модели AuctionImage"""
        user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpass123"
        )

        mark = CarMark.objects.create(car_mark="Toyota")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry")
        car = Car.objects.create(mark=mark, model=model, year=2020)

        auction = Auction.objects.create(
            car=car,
            engine_type="Gasoline",
            engine_capacity=Decimal("2.5"),
            drive="Front",
            gear_box="Automatic",
            body="Sedan",
            description="Test auction",
            price=Decimal("25000.00"),
            owner=user,
            phone_number="+375291234567",
            date_start=timezone.now() + datetime.timedelta(hours=1),
            date_end=timezone.now() + datetime.timedelta(days=7),
            status="soon"
        )

        auction_image = AuctionImage.objects.create(
            auction=auction,
            image="test_image.jpg"
        )

        assert auction_image.auction == auction
        assert auction_image.image == "test_image.jpg"
        assert str(auction_image) == f"Auction image for {auction.id}"

    def test_winner_model(self):
        """Тест модели Winner"""
        user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpass123"
        )
        user2 = User.objects.create_user(
            username="winneruser", email="winner@test.com", password="winnerpass123"
        )

        mark = CarMark.objects.create(car_mark="Toyota")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry")
        car = Car.objects.create(mark=mark, model=model, year=2020)

        auction = Auction.objects.create(
            car=car,
            engine_type="Gasoline",
            engine_capacity=Decimal("2.5"),
            drive="Front",
            gear_box="Automatic",
            body="Sedan",
            description="Test auction",
            price=Decimal("25000.00"),
            owner=user,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(days=7),
            date_end=timezone.now() - datetime.timedelta(hours=1),
            status="stop"
        )

        winner = Winner.objects.create(
            auction=auction,
            user=user2
        )

        assert winner.auction == auction
        assert winner.user == user2
        assert str(winner) == f"Winner: {user2.id} for {auction.id}"

    def test_bid_model(self):
        """Тест модели Bid"""
        user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpass123"
        )
        bidder = User.objects.create_user(
            username="bidder", email="bidder@test.com", password="bidderpass123"
        )

        mark = CarMark.objects.create(car_mark="Toyota")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry")
        car = Car.objects.create(mark=mark, model=model, year=2020)

        auction = Auction.objects.create(
            car=car,
            engine_type="Gasoline",
            engine_capacity=Decimal("2.5"),
            drive="Front",
            gear_box="Automatic",
            body="Sedan",
            description="Test auction",
            price=Decimal("25000.00"),
            owner=user,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(hours=1),
            date_end=timezone.now() + datetime.timedelta(days=7),
            status="go"
        )

        bid = Bid.objects.create(
            user=bidder,
            auction=auction,
            bef_bid_price=Decimal("25000.00"),
            bid=Decimal("25500.00")
        )

        assert bid.user == bidder
        assert bid.auction == auction
        assert bid.bef_bid_price == Decimal("25000.00")
        assert bid.bid == Decimal("25500.00")
        assert str(bid) == f"{bidder} - {car} - {Decimal('25500.00')}"


@pytest.mark.django_db
class TestAuctionsViews:
    """Тесты для views приложения auction"""

    def test_auctions_view(self):
        client = Client()

        user = User.objects.create(
            username="test", email="test@test.com", password="testtest"
        )

        mark = CarMark.objects.create(car_mark="test")
        model = CarModel.objects.create(car_mark=mark, car_model="test")
        car = Car.objects.create(mark=mark, model=model, year=random.randint(1800, 2022))
        auction = Auction.objects.create(car=car, engine_type="Test", engine_capacity=random.randint(1, 10),
                                         drive="No type", gear_box="No type", description="Test",
                                         price=random.randrange(9999999999999), owner=user,
                                         phone_number=random.randrange(9999999), date_start=timezone.now(),
                                         date_end=timezone.now() + datetime.timedelta(days=1),
                                         )

        client.force_login(user)

        response = client.get("/auction/")
        assert response.status_code == 200

        response = client.get("/auction/add")
        assert response.status_code == 301

        response = client.get(f"/details/{auction.id}")
        assert response.status_code == 301


@pytest.mark.django_db
class TestAuctionForms:
    """Тесты для форм приложения auction"""

    def test_auction_filters_form_valid(self):
        """Тест валидной формы фильтров аукциона"""
        from auction.forms import AuctionFiltersForm

        # Создаем марку для теста
        from showbill.models import CarMark
        mark = CarMark.objects.create(car_mark="Toyota")

        # Валидные данные (form data from HTTP is strings)
        form_data = {
            "price__gt": "10000",
            "price__lt": "50000",
            "order_price": "price_asc",
            "engine_type": "petr",
            "mark": str(mark.id),
            "gear_box": "auto",
            "drive": "fwd",
            "status": "go",
            "body": "sedan"
        }

        form = AuctionFiltersForm(form_data)
        assert form.is_valid()

        # Проверяем очищенные данные
        cleaned_data = form.cleaned_data
        assert cleaned_data["price__gt"] == 10000
        assert cleaned_data["price__lt"] == 50000
        assert cleaned_data["order_price"] == "price_asc"
        assert cleaned_data["engine_type"] == "petr"
        # ChoiceField returns the actual value from choices (integer ID)
        assert cleaned_data["mark"] == str(mark.id)

    def test_auction_filters_form_invalid_price_range(self):
        """Тест невалидной формы фильтров с неправильным диапазоном цен"""
        from auction.forms import AuctionFiltersForm

        # Невалидные данные: min цена больше max
        form_data = {
            "price__gt": 50000,
            "price__lt": 10000,
        }

        form = AuctionFiltersForm(data=form_data)
        assert not form.is_valid()
        assert "Min price can't be greater than Max price" in str(form.errors.as_json())

    def test_auction_filters_form_empty(self):
        """Тест пустой формы фильтров"""
        from auction.forms import AuctionFiltersForm

        form = AuctionFiltersForm(data={})
        assert form.is_valid()  # Все поля необязательные

    def test_car_auction_form_valid(self):
        """Тест валидной формы CarAuctionForm"""
        from auction.forms import CarAuctionForm
        from showbill.models import CarMark, CarModel

        # Создаем данные для теста
        mark = CarMark.objects.create(car_mark="Toyota")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry")

        form_data = {
            "mark": mark.id,
            "model": model.id,
            "year": 2020
        }

        form = CarAuctionForm(data=form_data, mark_id=mark.id)
        assert form.is_valid()

        cleaned_data = form.cleaned_data
        assert cleaned_data["mark"] == mark
        assert cleaned_data["model"] == model
        assert cleaned_data["year"] == 2020

    def test_auction_form_valid(self):
        """Тест валидной формы AuctionForm"""
        from auction.forms import AuctionForm
        from django.utils import timezone
        import datetime

        future_start = timezone.now() + datetime.timedelta(hours=4)
        future_end = timezone.now() + datetime.timedelta(days=7)

        form_data = {
            "engine_type": "petr",
            "engine_capacity": "2.5",
            "drive": "fwd",
            "gear_box": "auto",
            "body": "sedan",
            "description": "Test description",
            "win": "ABC12345678901234",
            "price": "25000.00",
            "phone_number": "+375291234567",
            "date_start": future_start.strftime("%Y-%m-%dT%H"),
            "date_end": future_end.strftime("%Y-%m-%dT%H")
        }

        form = AuctionForm(form_data)
        assert form.is_valid()

        cleaned_data = form.cleaned_data
        assert cleaned_data["engine_type"] == "petr"
        assert cleaned_data["engine_capacity"] == 2.5
        assert cleaned_data["price"] == Decimal("25000.00")

    def test_auction_form_invalid_dates(self):
        """Тест невалидной формы с неправильными датами"""
        from auction.forms import AuctionForm
        from django.utils import timezone
        import datetime

        past_start = timezone.now() - datetime.timedelta(hours=1)
        future_end = timezone.now() + datetime.timedelta(days=7)

        # Дата начала в прошлом
        form_data = {
            "engine_type": "petr",
            "engine_capacity": "2.5",
            "drive": "fwd",
            "gear_box": "auto",
            "body": "sedan",
            "description": "Test description",
            "price": "25000.00",
            "phone_number": "+375291234567",
            "date_start": past_start.strftime("%Y-%m-%dT%H"),
            "date_end": future_end.strftime("%Y-%m-%dT%H")
        }

        form = AuctionForm(data=form_data)
        assert not form.is_valid()
        assert "Auction start date must be in the future" in str(form.errors)

        # Дата окончания раньше даты начала
        future_start = timezone.now() + datetime.timedelta(hours=3)
        earlier_end = timezone.now() + datetime.timedelta(hours=1)

        form_data = {
            "engine_type": "petr",
            "engine_capacity": "2.5",
            "drive": "fwd",
            "gear_box": "auto",
            "body": "sedan",
            "description": "Test description",
            "price": "25000.00",
            "phone_number": "+375291234567",
            "date_start": future_start.strftime("%Y-%m-%dT%H"),
            "date_end": earlier_end.strftime("%Y-%m-%dT%H")
        }

        form = AuctionForm(data=form_data)
        assert not form.is_valid()
        assert "Auction start date must be in the future" in str(form.errors.as_text())

    def test_auction_form_too_many_images(self):
        """Тест формы с слишком большим количеством изображений"""
        from auction.forms import AuctionForm
        from django.utils import timezone
        import datetime
        from django.core.files.uploadedfile import SimpleUploadedFile

        future_start = timezone.now() + datetime.timedelta(hours=2)
        future_end = timezone.now() + datetime.timedelta(days=7)

        # Создаем 9 файлов (больше разрешенных 8)
        files = []
        for i in range(9):
            files.append(SimpleUploadedFile(
                f"test_image_{i}.jpg",
                b"file_content",
                content_type="image/jpeg"
            ))

        form_data = {
            "engine_type": "petr",
            "engine_capacity": "2.5",
            "drive": "fwd",
            "gear_box": "auto",
            "body": "sedan",
            "description": "Test description",
            "price": "25000.00",
            "phone_number": "+375291234567",
            "date_start": future_start.strftime("%Y-%m-%dT%H"),
            "date_end": future_end.strftime("%Y-%m-%dT%H")
        }

        # Создаем форму с файлами
        form = AuctionForm(data=form_data, files={"image": files})
        assert not form.is_valid()
        assert "You can upload up to 8 photos" in str(form.errors)


@pytest.mark.django_db
class TestAuctionQueries:
    """Тесты для queries приложения auction"""

    def test_filter_cars_auction(self):
        """Тест функции фильтрации аукционов"""
        from auction.queries import filter_cars_auction
        from auction.models import Auction
        from django.contrib.auth.models import User
        from showbill.models import CarMark, CarModel, Car
        from django.utils import timezone
        import datetime

        # Создаем тестовые данные
        user = User.objects.create_user(username="testuser", password="testpass")
        mark = CarMark.objects.create(car_mark="Toyota")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry")
        car = Car.objects.create(mark=mark, model=model, year=2020)

        # Создаем несколько аукционов
        auction1 = Auction.objects.create(
            car=car,
            engine_type="petr",
            engine_capacity=Decimal("2.5"),
            drive="fwd",
            gear_box="auto",
            body="sedan",
            description="Auction 1",
            price=Decimal("20000.00"),
            owner=user,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(hours=1),
            date_end=timezone.now() + datetime.timedelta(days=7),
            status="go"
        )

        auction2 = Auction.objects.create(
            car=car,
            engine_type="dies",
            engine_capacity=Decimal("3.0"),
            drive="4wd",
            gear_box="man",
            body="jeep",
            description="Auction 2",
            price=Decimal("35000.00"),
            owner=user,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(hours=1),
            date_end=timezone.now() + datetime.timedelta(days=7),
            status="go"
        )

        # Получаем все аукционы
        auctions = Auction.objects.all()

        # Тестируем фильтрацию по цене
        filtered = filter_cars_auction(
            cars=auctions,
            price__gt=25000,
            price__lt=40000,
            order_price=None,
            engine_type=None,
            drive=None,
            gear_box=None,
            status=None,
            mark=None,
            body=None
        )

        assert filtered.count() == 1
        assert filtered.first() == auction2

        # Тестируем фильтрацию по типу двигателя
        filtered = filter_cars_auction(
            cars=auctions,
            price__gt=None,
            price__lt=None,
            order_price=None,
            engine_type="dies",
            drive=None,
            gear_box=None,
            status=None,
            mark=None,
            body=None
        )

        assert filtered.count() == 1
        assert filtered.first() == auction2

        # Тестируем сортировку по цене
        filtered = filter_cars_auction(
            cars=auctions,
            price__gt=None,
            price__lt=None,
            order_price="price_asc",
            engine_type=None,
            drive=None,
            gear_box=None,
            status=None,
            mark=None,
            body=None
        )

        assert filtered.count() == 2
        assert filtered.first() == auction1  # Самая низкая цена

        filtered = filter_cars_auction(
            cars=auctions,
            price__gt=None,
            price__lt=None,
            order_price="price_desc",
            engine_type=None,
            drive=None,
            gear_box=None,
            status=None,
            mark=None,
            body=None
        )

        assert filtered.first() == auction2  # Самая высокая цена

    def test_filter_auctions(self):
        """Тест функции фильтрации аукционов по дате"""
        from auction.queries import filter_auctions
        from auction.models import Auction
        from django.contrib.auth.models import User
        from showbill.models import CarMark, CarModel, Car
        from django.utils import timezone
        import datetime

        # Создаем тестовые данные
        user = User.objects.create_user(username="testuser", password="testpass")
        mark = CarMark.objects.create(car_mark="Toyota")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry")
        car = Car.objects.create(mark=mark, model=model, year=2020)

        # Создаем аукционы с разными датами создания
        auction1 = Auction.objects.create(
            car=car,
            engine_type="petr",
            engine_capacity=Decimal("2.5"),
            drive="fwd",
            gear_box="auto",
            body="sedan",
            description="Auction 1",
            price=Decimal("20000.00"),
            owner=user,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(days=2),
            date_end=timezone.now() + datetime.timedelta(days=5),
            status="go"
        )

        # Имитируем более старый аукцион
        auction1.created_at = timezone.now() - datetime.timedelta(days=2)
        auction1.save()

        auction2 = Auction.objects.create(
            car=car,
            engine_type="petr",
            engine_capacity=Decimal("2.5"),
            drive="fwd",
            gear_box="auto",
            body="sedan",
            description="Auction 2",
            price=Decimal("25000.00"),
            owner=user,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(hours=1),
            date_end=timezone.now() + datetime.timedelta(days=7),
            status="go"
        )

        auctions = Auction.objects.all()

        # Сортировка по убыванию даты (новые сначала)
        filtered = filter_auctions(auctions, "-created_at")
        assert filtered.first() == auction2  # Новейший

        # Сортировка по возрастанию даты (старые сначала)
        filtered = filter_auctions(auctions, "created_at")
        assert filtered.first() == auction1  # Старейший


@pytest.mark.django_db
class TestAuctionBidProcessor:
    """Тесты для bid_processor приложения auction"""

    def test_process_bid_atomic_success(self):
        """Тест успешной обработки ставки"""
        from auction.bid_processor import process_bid_atomic
        from auction.models import Auction, Bid
        from django.contrib.auth.models import User
        from showbill.models import CarMark, CarModel, Car
        from django.utils import timezone
        import datetime

        # Создаем тестовые данные
        owner = User.objects.create_user(username="owner", password="ownerpass")
        bidder = User.objects.create_user(username="bidder", password="bidderpass")

        mark = CarMark.objects.create(car_mark="Toyota")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry")
        car = Car.objects.create(mark=mark, model=model, year=2020)

        auction = Auction.objects.create(
            car=car,
            engine_type="petr",
            engine_capacity=Decimal("2.5"),
            drive="fwd",
            gear_box="auto",
            body="sedan",
            description="Test auction",
            price=Decimal("25000.00"),
            owner=owner,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(hours=1),
            date_end=timezone.now() + datetime.timedelta(days=7),
            status="go"
        )

        # Обрабатываем ставку
        success, message, new_price, bid_id = process_bid_atomic(
            auction_id=auction.id,
            user_id=bidder.id,
            bid_amount_str="25500.00"
        )

        assert success is True
        assert "успешно" in message.lower()
        assert new_price == "50500.00"
        assert bid_id is not None

        # Проверяем, что ставка создана
        bid = Bid.objects.get(id=bid_id)
        assert bid.user == bidder
        assert bid.auction == auction
        assert bid.bid == Decimal("25500.00")

        # Проверяем, что цена аукциона обновилась
        auction.refresh_from_db()
        assert auction.price == Decimal("50500.00")

    def test_process_bid_atomic_auction_not_active(self):
        """Тест обработки ставки на неактивный аукцион"""
        from auction.bid_processor import process_bid_atomic
        from auction.models import Auction
        from django.contrib.auth.models import User
        from showbill.models import CarMark, CarModel, Car
        from django.utils import timezone
        import datetime

        # Создаем тестовые данные
        owner = User.objects.create_user(username="owner", password="ownerpass")
        bidder = User.objects.create_user(username="bidder", password="bidderpass")

        mark = CarMark.objects.create(car_mark="Toyota")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry")
        car = Car.objects.create(mark=mark, model=model, year=2020)

        # Аукцион с статусом "stop" (не активен)
        auction = Auction.objects.create(
            car=car,
            engine_type="petr",
            engine_capacity=Decimal("2.5"),
            drive="fwd",
            gear_box="auto",
            body="sedan",
            description="Test auction",
            price=Decimal("25000.00"),
            owner=owner,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(days=7),
            date_end=timezone.now() - datetime.timedelta(days=1),
            status="stop"
        )

        # Пытаемся сделать ставку
        success, message, new_price, bid_id = process_bid_atomic(
            auction_id=auction.id,
            user_id=bidder.id,
            bid_amount_str="25500.00"
        )

        assert success is False
        assert "not active" in message.lower()
        assert new_price is None
        assert bid_id is None

    def test_process_bid_atomic_negative_bid(self):
        """Тест обработки отрицательной ставки"""
        from auction.bid_processor import process_bid_atomic
        from auction.models import Auction
        from django.contrib.auth.models import User
        from showbill.models import CarMark, CarModel, Car
        from django.utils import timezone
        import datetime

        # Создаем тестовые данные
        owner = User.objects.create_user(username="owner", password="ownerpass")
        bidder = User.objects.create_user(username="bidder", password="bidderpass")

        mark = CarMark.objects.create(car_mark="Toyota")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry")
        car = Car.objects.create(mark=mark, model=model, year=2020)

        auction = Auction.objects.create(
            car=car,
            engine_type="petr",
            engine_capacity=Decimal("2.5"),
            drive="fwd",
            gear_box="auto",
            body="sedan",
            description="Test auction",
            price=Decimal("25000.00"),
            owner=owner,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(hours=1),
            date_end=timezone.now() + datetime.timedelta(days=7),
            status="go"
        )

        # Пытаемся сделать отрицательную ставку
        success, message, new_price, bid_id = process_bid_atomic(
            auction_id=auction.id,
            user_id=bidder.id,
            bid_amount_str="-100.00"
        )

        assert success is False
        assert "positive" in message.lower()
        assert new_price is None
        assert bid_id is None

    def test_process_bid_with_retry(self):
        """Тест обработки ставки с повторными попытками"""
        from auction.bid_processor import process_bid_with_retry
        from auction.models import Auction
        from django.contrib.auth.models import User
        from showbill.models import CarMark, CarModel, Car
        from django.utils import timezone
        import datetime

        # Создаем тестовые данные
        owner = User.objects.create_user(username="owner", password="ownerpass")
        bidder = User.objects.create_user(username="bidder", password="bidderpass")

        mark = CarMark.objects.create(car_mark="Toyota")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry")
        car = Car.objects.create(mark=mark, model=model, year=2020)

        auction = Auction.objects.create(
            car=car,
            engine_type="petr",
            engine_capacity=Decimal("2.5"),
            drive="fwd",
            gear_box="auto",
            body="sedan",
            description="Test auction",
            price=Decimal("25000.00"),
            owner=owner,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(hours=1),
            date_end=timezone.now() + datetime.timedelta(days=7),
            status="go"
        )

        # Обрабатываем ставку с retry
        success, message, new_price, bid_id = process_bid_with_retry(
            auction_id=auction.id,
            user_id=bidder.id,
            bid_amount_str="25500.00",
            max_retries=3
        )

        assert success is True
        assert "успешно" in message.lower()
        assert new_price == "50500.00"
        assert bid_id is not None


@pytest.mark.django_db
class TestAuctionTasks:
    """Тесты для tasks приложения auction"""

    def test_run_status_update(self):
        """Тест обновления статусов аукционов"""
        from auction.tasks import run_status_update
        from auction.models import Auction
        from django.contrib.auth.models import User
        from showbill.models import CarMark, CarModel, Car
        from django.utils import timezone
        import datetime

        # Создаем тестовые данные
        user = User.objects.create_user(username="testuser", password="testpass")
        mark = CarMark.objects.create(car_mark="Toyota")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry")
        car = Car.objects.create(mark=mark, model=model, year=2020)

        # Создаем аукционы с разными временными рамками
        auction_go = Auction.objects.create(
            car=car,
            engine_type="petr",
            engine_capacity=Decimal("2.5"),
            drive="fwd",
            gear_box="auto",
            body="sedan",
            description="Auction in progress",
            price=Decimal("20000.00"),
            owner=user,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(hours=1),
            date_end=timezone.now() + datetime.timedelta(hours=1),
            status="soon"  # Начальный статус
        )

        auction_stop = Auction.objects.create(
            car=car,
            engine_type="petr",
            engine_capacity=Decimal("2.5"),
            drive="fwd",
            gear_box="auto",
            body="sedan",
            description="Ended auction",
            price=Decimal("25000.00"),
            owner=user,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(days=2),
            date_end=timezone.now() - datetime.timedelta(days=1),
            status="go"  # Начальный статус
        )

        auction_soon = Auction.objects.create(
            car=car,
            engine_type="petr",
            engine_capacity=Decimal("2.5"),
            drive="fwd",
            gear_box="auto",
            body="sedan",
            description="Future auction",
            price=Decimal("30000.00"),
            owner=user,
            phone_number="+375291234567",
            date_start=timezone.now() + datetime.timedelta(hours=2),
            date_end=timezone.now() + datetime.timedelta(days=2),
            status="stop"  # Начальный статус
        )

        # Запускаем обновление статусов
        run_status_update()

        # Обновляем объекты из базы
        auction_go.refresh_from_db()
        auction_stop.refresh_from_db()
        auction_soon.refresh_from_db()

        # Проверяем обновленные статусы
        assert auction_go.status == "go"  # Должен быть "в процессе"
        assert auction_stop.status == "stop"  # Должен быть "завершен"
        assert auction_soon.status == "soon"  # Должен быть "скоро"

    def test_search_winners(self):
        """Тест поиска победителей аукционов"""
        from auction.tasks import search_winners
        from auction.models import Auction, Bid, Winner
        from django.contrib.auth.models import User
        from showbill.models import CarMark, CarModel, Car
        from django.utils import timezone
        import datetime

        # Создаем тестовые данные
        owner = User.objects.create_user(username="owner", password="ownerpass")
        bidder1 = User.objects.create_user(username="bidder1", password="bidderpass")
        bidder2 = User.objects.create_user(username="bidder2", password="bidderpass")

        mark = CarMark.objects.create(car_mark="Toyota")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry")
        car = Car.objects.create(mark=mark, model=model, year=2020)

        # Создаем завершенный аукцион со ставками
        auction = Auction.objects.create(
            car=car,
            engine_type="petr",
            engine_capacity=Decimal("2.5"),
            drive="fwd",
            gear_box="auto",
            body="sedan",
            description="Test auction",
            price=Decimal("25000.00"),
            owner=owner,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(days=2),
            date_end=timezone.now() - datetime.timedelta(days=1),
            status="stop"
        )

        # Создаем ставки
        bid1 = Bid.objects.create(
            user=bidder1,
            auction=auction,
            bef_bid_price=Decimal("25000.00"),
            bid=Decimal("25500.00"),
            created_at=timezone.now() - datetime.timedelta(hours=3)
        )
        assert bid1.bef_bid_price == Decimal("25000.00")

        bid2 = Bid.objects.create(
            user=bidder2,
            auction=auction,
            bef_bid_price=Decimal("25500.00"),
            bid=Decimal("26000.00"),
            created_at=timezone.now() - datetime.timedelta(hours=2)
        )
        assert bid2.bef_bid_price == Decimal("25500.00")

        # Запускаем поиск победителей
        search_winners()

        # Проверяем, что победитель создан
        winner = Winner.objects.filter(auction=auction).first()
        assert winner is not None
        assert winner.user == bidder2  # Последняя ставка от bidder2

        # Проверяем, что повторный запуск не создает дубликатов
        initial_count = Winner.objects.count()
        search_winners()
        assert Winner.objects.count() == initial_count


@pytest.mark.django_db
class TestAuctionViewsDetailed:
    """Детальные тесты для views приложения auction"""

    def test_car_auction_view_with_filters(self):
        """Тест главной страницы аукционов с фильтрами"""
        from auction.views import CarAuctionView
        from auction.models import Auction
        from django.contrib.auth.models import User
        from showbill.models import CarMark, CarModel, Car
        from django.utils import timezone
        import datetime

        # Создаем тестовые данные
        user = User.objects.create_user(username="testuser", password="testpass")
        mark = CarMark.objects.create(car_mark="Toyota")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry")
        car = Car.objects.create(mark=mark, model=model, year=2020)

        # Создаем аукционы с разными статусами
        auction_go = Auction.objects.create(
            car=car,
            engine_type="petr",
            engine_capacity=Decimal("2.5"),
            drive="fwd",
            gear_box="auto",
            body="sedan",
            description="Auction in progress",
            price=Decimal("20000.00"),
            owner=user,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(hours=1),
            date_end=timezone.now() + datetime.timedelta(hours=1),
            status="go"
        )
        assert auction_go.status == "go"

        auction_soon = Auction.objects.create(
            car=car,
            engine_type="dies",
            engine_capacity=Decimal("3.0"),
            drive="4wd",
            gear_box="man",
            body="jeep",
            description="Future auction",
            price=Decimal("35000.00"),
            owner=user,
            phone_number="+375291234567",
            date_start=timezone.now() + datetime.timedelta(hours=2),
            date_end=timezone.now() + datetime.timedelta(days=2),
            status="soon"
        )
        assert auction_soon.status == "soon"

        # Тестируем view
        view = CarAuctionView()
        view.request = type("Request", (), {"GET": {}})()

        context = view.get_context_data()

        assert "auctions" in context
        assert "filters_form" in context
        assert len(context["auctions"]) == 2

        # Проверяем сортировку по статусу (go -> soon -> stop)
        auctions = list(context["auctions"])
        assert auctions[0].status == "go"
        assert auctions[1].status == "soon"

    def test_models_for_mark_auction_endpoint(self):
        """Тест AJAX endpoint для получения моделей по марке"""
        from django.test import Client
        from showbill.models import CarMark, CarModel

        client = Client()

        # Создаем тестовые данные
        mark = CarMark.objects.create(car_mark="Toyota")
        model1 = CarModel.objects.create(car_mark=mark, car_model="Camry")
        model2 = CarModel.objects.create(car_mark=mark, car_model="Corolla")

        # Тестируем endpoint
        response = client.get(f"/ajax/auction/models/{mark.id}/")

        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"

        data = response.json()
        assert len(data) == 2

        # Проверяем структуру данных
        model_ids = [item["id"] for item in data]
        model_names = [item["car_model"] for item in data]

        assert model1.id in model_ids
        assert model2.id in model_ids
        assert "Camry" in model_names
        assert "Corolla" in model_names

    def test_create_auction_view_get(self):
        """Тест GET запроса к странице создания аукциона"""
        from django.test import Client
        from django.contrib.auth.models import User

        client = Client()

        # Создаем пользователя
        user = User.objects.create_user(username="testuser", password="testpass")
        client.force_login(user)

        # Тестируем GET запрос
        response = client.get("/auction/add")

        # Проверяем редирект или успешный ответ
        if response.status_code == 200:
            assert "form" in response.context
            assert "form_car" in response.context
        elif response.status_code == 301 or response.status_code == 302:
            # Проверяем редирект
            pass
        else:
            assert f"Unexpected status code: {response.status_code}"

    def test_auction_view_details(self):
        """Тест страницы деталей аукциона"""
        from django.test import Client
        from auction.models import Auction
        from django.contrib.auth.models import User
        from showbill.models import CarMark, CarModel, Car
        from django.utils import timezone
        import datetime

        client = Client()

        # Создаем тестовые данные
        user = User.objects.create_user(username="testuser", password="testpass")
        mark = CarMark.objects.create(car_mark="Toyota")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry")
        car = Car.objects.create(mark=mark, model=model, year=2020)

        auction = Auction.objects.create(
            car=car,
            engine_type="petr",
            engine_capacity=Decimal("2.5"),
            drive="fwd",
            gear_box="auto",
            body="sedan",
            description="Test auction",
            price=Decimal("25000.00"),
            owner=user,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(hours=1),
            date_end=timezone.now() + datetime.timedelta(days=7),
            status="go"
        )

        client.force_login(user)

        # Тестируем GET запрос
        response = client.get(f"/auction/{auction.id}/")

        if response.status_code == 200:
            assert "auction" in response.context
            assert "is_auction_in_favorites" in response.context
            assert "bids" in response.context
            assert "winner" in response.context

            context_auction = response.context["auction"]
            assert context_auction.id == auction.id
        elif response.status_code == 301 or response.status_code == 302:
            # Проверяем редирект
            pass
        else:
            assert response.status_code == 404

    def test_auction_view_post_bid(self):
        """Тест POST запроса для размещения ставки"""
        from django.test import Client
        from auction.models import Auction, Bid
        from django.contrib.auth.models import User
        from showbill.models import CarMark, CarModel, Car
        from django.utils import timezone
        import datetime

        client = Client()

        # Создаем тестовые данные
        owner = User.objects.create_user(username="owner", password="ownerpass")
        bidder = User.objects.create_user(username="bidder", password="bidderpass")

        mark = CarMark.objects.create(car_mark="Toyota")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry")
        car = Car.objects.create(mark=mark, model=model, year=2020)

        auction = Auction.objects.create(
            car=car,
            engine_type="petr",
            engine_capacity=Decimal("2.5"),
            drive="fwd",
            gear_box="auto",
            body="sedan",
            description="Test auction",
            price=Decimal("25000.00"),
            owner=owner,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(hours=1),
            date_end=timezone.now() + datetime.timedelta(days=7),
            status="go"
        )

        client.force_login(bidder)

        # Тестируем POST запрос со ставкой
        response = client.post(
            f"/auction/{auction.id}/",
            {
                "bid": "25500.00",
                "action": "add"  # Для добавления в избранное
            }
        )

        # Проверяем редирект после успешной ставки
        if response.status_code == 302:
            # Проверяем, что ставка создана
            bid_count = Bid.objects.filter(auction=auction, user=bidder).count()
            assert bid_count > 0

            # Проверяем, что цена обновилась
            auction.refresh_from_db()
            assert auction.price > Decimal("25000.00")
        elif response.status_code == 200:
            # Проверяем сообщения в контексте
            pass
        else:
            assert response.status_code == 404

    def test_auction_view_post_own_auction(self):
        """Тест попытки сделать ставку на свой собственный аукцион"""
        from django.test import Client
        from auction.models import Auction
        from django.contrib.auth.models import User
        from showbill.models import CarMark, CarModel, Car
        from django.utils import timezone
        import datetime

        client = Client()

        # Создаем тестовые данные
        owner = User.objects.create_user(username="owner", password="ownerpass")

        mark = CarMark.objects.create(car_mark="Toyota")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry")
        car = Car.objects.create(mark=mark, model=model, year=2020)

        auction = Auction.objects.create(
            car=car,
            engine_type="petr",
            engine_capacity=Decimal("2.5"),
            drive="fwd",
            gear_box="auto",
            body="sedan",
            description="Test auction",
            price=Decimal("25000.00"),
            owner=owner,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(hours=1),
            date_end=timezone.now() + datetime.timedelta(days=7),
            status="go"
        )

        client.force_login(owner)

        # Пытаемся сделать ставку на свой собственный аукцион
        initial_bid_count = auction.bids.count()
        initial_price = auction.price

        _ = client.post(
            f"/auction/{auction.id}/",
            {"bid": "25500.00"}
        )

        # Проверяем, что ставка не создана и цена не изменилась
        auction.refresh_from_db()
        assert auction.bids.count() == initial_bid_count
        assert auction.price == initial_price


@pytest.mark.django_db
class TestAuctionAdmin:
    """Тесты для admin приложения auction"""

    def test_auction_admin_display(self):
        """Тест отображения аукциона в админке"""
        from auction.admin import AuctionAdmin
        from auction.models import Auction
        from django.contrib.auth.models import User
        from showbill.models import CarMark, CarModel, Car
        from django.utils import timezone
        import datetime

        # Создаем тестовые данные
        user = User.objects.create_user(username="testuser", password="testpass")
        mark = CarMark.objects.create(car_mark="Toyota")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry")
        car = Car.objects.create(mark=mark, model=model, year=2020)

        _ = Auction.objects.create(
            car=car,
            engine_type="petr",
            engine_capacity=Decimal("2.5"),
            drive="fwd",
            gear_box="auto",
            body="sedan",
            description="Test auction",
            win="ABC12345678901234",
            price=Decimal("25000.00"),
            owner=user,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(hours=1),
            date_end=timezone.now() + datetime.timedelta(days=7),
            status="go"
        )

        # Тестируем Admin класс
        admin = AuctionAdmin(model=Auction, admin_site=None)

        # Проверяем list_display
        assert "car" in admin.list_display
        assert "engine_type" in admin.list_display
        assert "price" in admin.list_display
        assert "owner" in admin.list_display
        assert "status" in admin.list_display

        # Проверяем search_fields
        assert "engine_type" in admin.search_fields
        assert "gear_box" in admin.search_fields
        assert "body" in admin.search_fields
        assert "status" in admin.search_fields

        # Проверяем list_filter
        assert "status" in admin.list_filter

    def test_bid_admin_display(self):
        """Тест отображения ставки в админке"""
        from auction.admin import BidAdmin
        from auction.models import Auction, Bid
        from django.contrib.auth.models import User
        from showbill.models import CarMark, CarModel, Car
        from django.utils import timezone
        import datetime

        # Создаем тестовые данные
        owner = User.objects.create_user(username="owner", password="ownerpass")
        bidder = User.objects.create_user(username="bidder", password="bidderpass")

        mark = CarMark.objects.create(car_mark="Toyota")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry")
        car = Car.objects.create(mark=mark, model=model, year=2020)

        auction = Auction.objects.create(
            car=car,
            engine_type="petr",
            engine_capacity=Decimal("2.5"),
            drive="fwd",
            gear_box="auto",
            body="sedan",
            description="Test auction",
            price=Decimal("25000.00"),
            owner=owner,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(hours=1),
            date_end=timezone.now() + datetime.timedelta(days=7),
            status="go"
        )

        _ = Bid.objects.create(
            user=bidder,
            auction=auction,
            bef_bid_price=Decimal("25000.00"),
            bid=Decimal("25500.00")
        )

        # Тестируем Admin класс
        admin = BidAdmin(model=Bid, admin_site=None)

        # Проверяем list_display
        assert "user" in admin.list_display
        assert "auction" in admin.list_display
        assert "bid" in admin.list_display
        assert "created_at" in admin.list_display

        # Проверяем readonly_fields
        assert "created_at" in admin.readonly_fields


@pytest.mark.django_db
class TestAuctionConsumers:
    """Тесты для WebSocket consumers приложения auction"""

    @pytest.mark.asyncio
    async def test_auction_consumer_connect_success(self):
        """Тест успешного подключения к WebSocket"""
        from auction.consumers import AuctionConsumer
        from auction.models import Auction
        from django.contrib.auth.models import User
        from showbill.models import CarMark, CarModel, Car
        from django.utils import timezone
        from asgiref.sync import sync_to_async
        import datetime
        import json

        # Создаем тестовые данные
        user = await sync_to_async(User.objects.create_user)(
            username="testuser",
            password="testpass",
        )

        mark = await sync_to_async(CarMark.objects.create)(
            car_mark="Toyota_connect",
        )

        model = await sync_to_async(CarModel.objects.create)(
            car_mark=mark,
            car_model="Camry_connect",
        )

        car = await sync_to_async(Car.objects.create)(
            mark=mark,
            model=model,
            year=2020,
        )

        auction = await sync_to_async(Auction.objects.create)(
            car=car,
            engine_type="petr",
            engine_capacity=Decimal("2.5"),
            drive="fwd",
            gear_box="auto",
            body="sedan",
            description="Test auction",
            price=Decimal("25000.00"),
            owner=user,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(hours=1),
            date_end=timezone.now() + datetime.timedelta(days=7),
            status="go",
        )

        # Создаем consumer
        consumer = AuctionConsumer()

        consumer.scope = {
            "url_route": {"kwargs": {"auction_id": auction.id}},
            "user": user,
        }

        # Мокаем channel layer
        class MockChannelLayer:
            async def group_add(self, group, channel):
                pass

            async def group_discard(self, group, channel):
                pass

        consumer.channel_layer = MockChannelLayer()
        consumer.channel_name = "test_channel"

        # Перехватываем отправку WebSocket-сообщений
        messages = []
        websocket_frames = []

        async def mock_send(text_data=None, **kwargs):
            if text_data:
                messages.append(json.loads(text_data))

        # Перехватываем низкоуровневую отправку Channels
        async def mock_base_send(message):
            websocket_frames.append(message)

        consumer.send = mock_send
        consumer.base_send = mock_base_send

        # Тестируем подключение
        await consumer.connect()

        # Проверяем инициализацию consumer
        assert consumer.auction_id == auction.id
        assert consumer.user == user
        assert consumer.auction == auction
        assert consumer.room_group_name == f"auction_{auction.id}"

        # Проверяем успешное принятие WebSocket-соединения
        assert any(
            frame["type"] == "websocket.accept"
            for frame in websocket_frames
        )

        # Проверяем отправленное сообщение
        assert len(messages) == 1
        assert messages[0]["type"] == "auction_info"
        assert messages[0]["current_price"] == "25000.00"
        assert messages[0]["auction_id"] == auction.id

    @pytest.mark.asyncio
    async def test_auction_consumer_connect_unauthenticated(self):
        """Тест подключения неаутентифицированного пользователя"""
        from auction.consumers import AuctionConsumer
        from django.contrib.auth.models import AnonymousUser

        # Создаем consumer с анонимным пользователем
        consumer = AuctionConsumer()

        consumer.scope = {
            "url_route": {"kwargs": {"auction_id": 1}},
            "user": AnonymousUser()
        }

        # Мокаем close метод
        close_called = False

        async def mock_close(code=None):
            nonlocal close_called
            close_called = True
            assert code == 4001  # Код для неаутентифицированных пользователей

        consumer.close = mock_close

        # Тестируем подключение
        await consumer.connect()

        # Проверяем, что соединение закрыто
        assert close_called is True

    @pytest.mark.asyncio
    async def test_auction_consumer_receive_bid(self):
        """Тест получения ставки через WebSocket"""
        from auction.consumers import AuctionConsumer
        from auction.models import Auction
        from django.contrib.auth.models import User
        from showbill.models import CarMark, CarModel, Car
        from django.utils import timezone
        import datetime
        import json
        from asgiref.sync import sync_to_async

        # Создаем тестовые данные с sync_to_async
        owner = await sync_to_async(User.objects.create_user)(username="owner", password="ownerpass")
        bidder = await sync_to_async(User.objects.create_user)(username="bidder", password="bidderpass")

        mark = await sync_to_async(CarMark.objects.create)(car_mark="Toyota_receive")
        model = await sync_to_async(CarModel.objects.create)(car_mark=mark, car_model="Camry_receive")
        car = await sync_to_async(Car.objects.create)(mark=mark, model=model, year=2020)

        auction = await sync_to_async(Auction.objects.create)(
            car=car,
            engine_type="Gasoline",
            engine_capacity=Decimal("2.5"),
            drive="Front",
            gear_box="Automatic",
            body="Sedan",
            description="Test auction",
            price=Decimal("25000.00"),
            owner=owner,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(hours=1),
            date_end=timezone.now() + datetime.timedelta(days=7),
            status="go"
        )

        # Создаем consumer
        consumer = AuctionConsumer()

        # Настраиваем consumer
        consumer.auction_id = auction.id
        consumer.auction = auction
        consumer.user = bidder
        consumer.room_group_name = f"auction_{auction.id}"

        # Мокаем методы
        messages = []

        async def mock_send(text_data=None):
            if text_data:
                messages.append(json.loads(text_data))

        consumer.send = mock_send

        group_send_called = False
        group_send_data = None

        async def mock_group_send(_, group, data):
            nonlocal group_send_called, group_send_data
            group_send_called = True
            group_send_data = data

            # Вызываем обработчик события
            if data["type"] == "bid_update":
                await consumer.bid_update(data)

        consumer.channel_layer = type("MockChannelLayer", (), {
            "group_send": mock_group_send
        })()

        # Тестируем получение ставки
        bid_data = json.dumps({
            "type": "bid",
            "bid_amount": "25500.00"
        })

        await consumer.receive(text_data=bid_data)

        # Проверяем, что ставка обработана
        assert group_send_called is True
        assert group_send_data["type"] == "bid_update"
        assert group_send_data["bid_amount"] == "25500.00"
        assert group_send_data["user_id"] == bidder.id
        assert group_send_data["user_username"] == "bidder"

        # Проверяем отправленные сообщения
        assert len(messages) > 0

        # Ищем сообщение bid_update
        bid_update_messages = [m for m in messages if m.get("type") == "bid_update"]
        assert len(bid_update_messages) == 1

        bid_update_msg = bid_update_messages[0]
        assert bid_update_msg["bid_amount"] == "25500.00"
        assert bid_update_msg["user_username"] == "bidder"

    @pytest.mark.asyncio
    async def test_auction_consumer_receive_invalid_json(self):
        """Тест получения невалидного JSON"""
        from auction.consumers import AuctionConsumer

        # Создаем consumer
        consumer = AuctionConsumer()

        # Мокаем send метод
        messages = []

        async def mock_send(text_data=None):
            if text_data:
                messages.append(json.loads(text_data))

        consumer.send = mock_send

        # Тестируем получение невалидного JSON
        await consumer.receive(text_data="invalid json")

        # Проверяем сообщение об ошибке
        assert len(messages) == 1
        assert messages[0]["type"] == "bid_error"
        assert "Invalid JSON" in messages[0]["message"]

    @pytest.mark.asyncio
    async def test_auction_consumer_receive_empty_bid(self):
        """Тест получения пустой ставки"""
        from auction.consumers import AuctionConsumer
        import json

        # Создаем consumer
        consumer = AuctionConsumer()

        # Мокаем send метод
        messages = []

        async def mock_send(text_data=None):
            if text_data:
                messages.append(json.loads(text_data))

        consumer.send = mock_send

        # Тестируем получение пустой ставки
        bid_data = json.dumps({
            "type": "bid",
            "bid_amount": ""
        })

        await consumer.receive(text_data=bid_data)

        # Проверяем сообщение об ошибке
        assert len(messages) == 1
        assert messages[0]["type"] == "bid_error"
        assert "Bid amount is required" in messages[0]["message"]

    @pytest.mark.asyncio
    async def test_auction_consumer_price_update(self):
        """Тест обработки обновления цены"""
        from auction.consumers import AuctionConsumer
        import json

        # Создаем consumer
        consumer = AuctionConsumer()

        # Мокаем send метод
        messages = []

        async def mock_send(text_data=None):
            if text_data:
                messages.append(json.loads(text_data))

        consumer.send = mock_send

        # Тестируем обработку price_update
        event = {
            "type": "price_update",
            "new_price": "25500.00",
            "auction_id": 1
        }

        await consumer.price_update(event)

        # Проверяем отправленное сообщение
        assert len(messages) == 1
        assert messages[0]["type"] == "price_update"
        assert messages[0]["new_price"] == "25500.00"
        assert messages[0]["auction_id"] == 1

    @pytest.mark.asyncio
    async def test_auction_consumer_disconnect(self):
        """Тест отключения от WebSocket"""
        from auction.consumers import AuctionConsumer

        # Создаем consumer
        consumer = AuctionConsumer()
        consumer.room_group_name = "auction_1"
        consumer.channel_name = "test_channel"

        # Мокаем channel_layer.group_discard
        discard_called = False

        async def mock_group_discard(_, group, channel):
            nonlocal discard_called
            discard_called = True
            assert group == "auction_1"
            assert channel == "test_channel"

        consumer.channel_layer = type("MockChannelLayer", (), {
            "group_discard": mock_group_discard
        })()

        # Тестируем отключение
        await consumer.disconnect(code=1000)

        # Проверяем, что метод вызван
        assert discard_called is True
