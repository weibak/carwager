def filter_cars_auction(cars, price__gt, price__lt, order_price, engine_type, drive, gear_box, status, mark, body):
    if price__gt is not None:
        cars = cars.filter(price__gt=price__gt)
    if price__lt is not None:
        cars = cars.filter(price__lt=price__lt)
    if order_price:
        if order_price == "price_asc":
            cars = cars.order_by("price")
        if order_price == "price_desc":
            cars = cars.order_by("-price")
    if engine_type:
        cars = cars.filter(engine_type=engine_type)

    if drive:
        cars = cars.filter(drive=drive)

    if gear_box:
        cars = cars.filter(gear_box=gear_box)

    if status:
        cars = cars.filter(status=status)

    if mark:
        cars = cars.filter(car__mark=mark)

    if body:
        cars = cars.filter(body=body)
    return cars


def filter_auctions(auctions, order_date):
    if order_date == "-created_at":
        auctions = auctions.order_by("-created_at")
    elif order_date == "created_at":
        auctions = auctions.order_by("created_at")
    return auctions
