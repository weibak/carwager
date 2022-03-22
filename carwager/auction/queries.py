def filter_cars_auction(cars, price__gt, price__lt, order_by, engine_type, drive, gear_box):
    if price__gt is not None:
        cars = cars.filter(price__gt=price__gt)
    if price__lt is not None:
        cars = cars.filter(price__lt=price__lt)
    if order_by:
        if order_by == "price_asc":
            cars = cars.order_by("price")
        if order_by == "cost_desc":
            cars = cars.order_by("-price")
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
        if engine_type == "fwd":
            cars = cars.filter(drive="fwd")
        if engine_type == "rwd":
            cars = cars.filter(drive="rwd")
        if engine_type == "awd":
            cars = cars.filter(drive="awd")
        if engine_type == "4wd":
            cars = cars.filter(drive="4wd")
    if gear_box:
        if engine_type == "auto":
            cars = cars.filter(gear_box="auto")
        if engine_type == "man":
            cars = cars.filter(gear_box="man")
    return cars


def filter_auctions(auctions, order_by):
    if order_by == "-created_at":
        auctions = auctions.order_by("-created_at")
    elif order_by == "created_at":
        auctions = auctions.order_by("created_at")
    return auctions
