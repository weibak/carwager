def filter_cars(cars, price__gt, price__lt, order_by, mark, engine_type, drive, gear_box):
    if price__gt is not None:
        cars = cars.filter(price__gt=price__gt)
    if price__lt is not None:
        cars = cars.filter(price__lt=price__lt)
    if order_by is not None:
        if order_by == "price_asc":
            cars = cars.order_by("price")
        if order_by == "cost_desc":
            cars = cars.order_by("-price")
    if mark is not None:
        if mark == "bmw":
            cars = cars.filter(mark="bmw")
        if mark == "merc":
            cars = cars.filter(mark="merc")
        if mark == "toyo":
            cars = cars.filter(mark="toyo")
    if engine_type is not None:
        if engine_type == "petr":
            cars = cars.filter(engine_type="petr")
        if engine_type == "dies":
            cars = cars.filter(engine_type="dies")
        if engine_type == "hyb":
            cars = cars.filter(engine_type="hyb")
        if engine_type == "elec":
            cars = cars.filter(engine_type="elec")
    if drive is not None:
        if drive == "fwd":
            cars = cars.filter(drive="fwd")
        if drive == "rwd":
            cars = cars.filter(drive="rwd")
        if drive == "awd":
            cars = cars.filter(drive="awd")
        if drive == "4wd":
            cars = cars.filter(drive="4wd")
    if gear_box is not None:
        if gear_box == "auto":
            cars = cars.filter(gear_box="auto")
        if gear_box == "man":
            cars = cars.filter(gear_box="man")
    return cars


def filter_adverts(adverts, order_by):
    if order_by == "-created_at":
        adverts = adverts.order_by("-created_at")
    elif order_by == "created_at":
        adverts = adverts.order_by("created_at")
    return adverts
