from django.db.models import Sum, F


def filter_cars(products, cost__gt, cost__lt, order_by):
    if cost__gt is not None:
        products = products.filter(cost__gt=cost__gt)
    if cost__lt is not None:
        products = products.filter(cost__lt=cost__lt)
    if order_by:
        if order_by == "cost_asc":
            products = products.order_by("cost")
        if order_by == "cost_desc":
            products = products.order_by("-cost")
        if order_by == "max_price":
            products = products.annotate(
                total_cost=Sum("purchases__count") * F("cost")
            ).order_by("-total_cost")
    return products


def filter_purchases(purchases, order_by):
    if order_by == "-created_at":
        purchases = purchases.order_by("-created_at")
    elif order_by == "created_at":
        purchases = purchases.order_by("created_at")
    return purchases
