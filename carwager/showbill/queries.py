def filter_cars(cars, price__gt, price__lt, order_price, mark, engine_type, drive, gear_box):
    if price__gt is not None:
        cars = cars.filter(price__gt=price__gt)
        return cars
    if price__lt is not None:
        cars = cars.filter(price__lt=price__lt)
        return cars
    if order_price:
        if order_price == "price_asc":
            cars = cars.order_by("price")
        if order_price == "price_desc":
            cars = cars.order_by("-price")
    if mark:
        if mark == "bmw":
            cars = cars.filter(car__mark__car_mark="BMW")
        if mark == "merc":
            cars = cars.filter(car__mark__car_mark="MERCEDES")
        if mark == "toyo":
            cars = cars.filter(car__mark__car_mark="TOYOTA")
    if engine_type:
        if engine_type == "petr":
            cars = cars.filter(engine_type="petr")
        if engine_type == "dies":
            cars = cars.filter(engine_type="dies")
        if engine_type == "hyb":
            cars = cars.filter(engine_type="hyb")
        if engine_type == "elec":
            cars = cars.filter(engine_type="elec")
    if drive:
        if drive == "fwd":
            cars = cars.filter(drive="fwd")
        if drive == "rwd":
            cars = cars.filter(drive="rwd")
        if drive == "awd":
            cars = cars.filter(drive="awd")
        if drive == "4wd":
            cars = cars.filter(drive="4wd")
    if gear_box:
        if gear_box == "auto":
            cars = cars.filter(gear_box="auto")
        if gear_box == "man":
            cars = cars.filter(gear_box="man")
    return cars


def filter_adverts(adverts, order_date):
    if order_date == "-created_at":
        adverts = adverts.order_by("-created_at")
    elif order_date == "created_at":
        adverts = adverts.order_by("created_at")
    return adverts
