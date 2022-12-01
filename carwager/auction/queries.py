def filter_cars_auction(cars, price__gt, price__lt, order_price, engine_type, drive, gear_box, status):
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
    if status:
        if status == "go":
            cars = cars.filter(status="go")
        if status == "stop":
            cars = cars.filter(status="stop")
        if status == "soon":
            cars = cars.filter(status="soon")
    return cars


def filter_auctions(auctions, order_date):
    if order_date == "-created_at":
        auctions = auctions.order_by("-created_at")
    elif order_date == "created_at":
        auctions = auctions.order_by("created_at")
    return auctions
