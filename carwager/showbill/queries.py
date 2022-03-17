from django.db.models import Sum, F


def filter_cars(cars, price__gt, price__lt, order_by):
    if price__gt is not None:
        cars = cars.filter(price__gt=price__gt)
    if price__lt is not None:
        cars = cars.filter(price__lt=price__lt)
    if order_by:
        if order_by == "price_asc":
            cars = cars.order_by("price")
        if order_by == "cost_desc":
            cars = cars.order_by("-price")

    return cars


def filter_adverts(purchases, order_by):
    if order_by == "-created_at":
        purchases = purchases.order_by("-created_at")
    elif order_by == "created_at":
        purchases = purchases.order_by("created_at")
    return purchases
