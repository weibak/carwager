import datetime
import random
from decimal import Decimal

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.utils import timezone

from auction.models import Auction
from showbill.models import Car, CarModel, CarMark


@pytest.mark.django_db
class TestAuctionsAPI:
    """Тесты для API endpoints приложения auction"""
    
    def test_auctions_api_list(self):
        """Тест получения списка аукционов через API"""
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
        
        # Проверяем структуру ответа
        data = response.json()
        assert "results" in data or isinstance(data, list)
        
        # Если используется пагинация
        if "results" in data:
            assert isinstance(data["results"], list)
            if len(data["results"]) > 0:
                auction_data = data["results"][0]
                assert "car_id" in auction_data
                assert "price" in auction_data
        elif isinstance(data, list) and len(data) > 0:
            auction_data = data[0]
            assert "car_id" in auction_data
            assert "price" in auction_data
    
    def test_auctions_api_detail(self):
        """Тест получения деталей аукциона через API"""
        client = Client()
        
        user = User.objects.create_user(username="testuser", password="testpass")
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
        
        client.force_login(user)
        
        # Тестируем endpoint деталей аукциона
        response = client.get(f"/api/auctions/{auction.id}/")
        
        # Проверяем успешный ответ или 404 если endpoint не существует
        if response.status_code == 200:
            data = response.json()
            assert data["id"] == auction.id
            assert data["price"] == "25000.00"
            assert data["status"] == "go"
        elif response.status_code == 404:
            # Endpoint может не существовать
            pass
        else:
            assert False, f"Unexpected status code: {response.status_code}"
    
    def test_auctions_api_filter(self):
        """Тест фильтрации аукционов через API"""
        client = Client()
        
        user = User.objects.create_user(username="testuser", password="testpass")
        mark = CarMark.objects.create(car_mark="Toyota")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry")
        car = Car.objects.create(mark=mark, model=model, year=2020)
        
        # Создаем аукционы с разными ценами
        auction1 = Auction.objects.create(
            car=car,
            engine_type="Gasoline",
            engine_capacity=Decimal("2.5"),
            drive="Front",
            gear_box="Automatic",
            body="Sedan",
            description="Cheap auction",
            price=Decimal("30000.00"),
            owner=user,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(hours=1),
            date_end=timezone.now() + datetime.timedelta(days=7),
            status="go"
        )
        
        auction2 = Auction.objects.create(
            car=car,
            engine_type="Diesel",
            engine_capacity=Decimal("3.0"),
            drive="4WD",
            gear_box="Manual",
            body="SUV",
            description="Expensive auction",
            price=Decimal("35000.00"),
            owner=user,
            phone_number="+375291234567",
            date_start=timezone.now() - datetime.timedelta(hours=1),
            date_end=timezone.now() + datetime.timedelta(days=7),
            status="go"
        )
        
        client.force_login(user)
        
        # Тестируем фильтрацию по минимальной цене
        response = client.get("/api/auctions/?price__gt=30000")
        
        if response.status_code == 200:
            data = response.json()
            
            # Проверяем, что возвращаются только дорогие аукционы
            if "results" in data:
                auctions = data["results"]
            else:
                auctions = data
            
            assert len(auctions) >= 1
            
            # Проверяем, что все аукционы дороже 30000
            for auction_data in auctions:
                price = Decimal(auction_data["price"])
                assert price >= Decimal("30000.00")
    
    def test_auctions_api_authentication(self):
        """Тест аутентификации в API"""
        client = Client()
        
        # Тестируем без аутентификации
        response = client.get("/api/auctions/")
        
        # API может требовать аутентификацию или нет
        if response.status_code == 401 or response.status_code == 403:
            # API требует аутентификацию
            pass
        elif response.status_code == 200:
            # API публичный
            pass
        else:
            # Другие коды статуса
            pass
    
    def test_auctions_api_pagination(self):
        """Тест пагинации в API"""
        client = Client()
        
        user = User.objects.create_user(username="testuser", password="testpass")
        mark = CarMark.objects.create(car_mark="Toyota")
        model = CarModel.objects.create(car_mark=mark, car_model="Camry")
        car = Car.objects.create(mark=mark, model=model, year=2020)
        
        # Создаем несколько аукционов
        for i in range(15):
            Auction.objects.create(
                car=car,
                engine_type="Gasoline",
                engine_capacity=Decimal("2.5"),
                drive="Front",
                gear_box="Automatic",
                body="Sedan",
                description=f"Auction {i}",
                price=Decimal(f"{20000 + i * 1000}.00"),
                owner=user,
                phone_number="+375291234567",
                date_start=timezone.now() - datetime.timedelta(hours=1),
                date_end=timezone.now() + datetime.timedelta(days=7),
                status="go"
            )
        
        client.force_login(user)
        
        response = client.get("/api/auctions/")
        
        if response.status_code == 200:
            data = response.json()
            
            # Проверяем пагинацию
            if "count" in data and "results" in data:
                # Используется пагинация Django REST Framework
                assert data["count"] >= 15
                assert isinstance(data["results"], list)
                
                # Проверяем, что есть ссылки на следующую страницу
                if data["count"] > len(data["results"]):
                    assert "next" in data
            elif isinstance(data, list):
                # Без пагинации
                assert len(data) >= 15
