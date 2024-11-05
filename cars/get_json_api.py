from collections import defaultdict
from .calculate_car_price import get_config, calc_price
from bs4 import BeautifulSoup
from .models import Currency, ColorTag, PrivodTag


def get_car(html_text: str, table: str):
    currency = Currency.objects.all()[0]
    config = get_config()

    soup = BeautifulSoup(html_text, "lxml-xml")
    root = soup.find("aj")
    rows = root.find_all("row")
    list_car = []

    if table == 'main':
        country = 'Корея'
    elif table == 'china':
        country = 'Китай'
    else:
        country = 'Япония'

    color_tags_dict = defaultdict(str)

    color_tags = ColorTag.objects.select_related('color').filter(color__country=country)

    for color_tag in color_tags:
        color_tags_dict[color_tag.name] = color_tag.color.name

    priv_tags_dict = defaultdict(str)

    priv_tags = PrivodTag.objects.select_related('privod').all()

    for priv_tag in priv_tags:
        priv_tags_dict[priv_tag.name] = priv_tag.privod.name

    for row in rows:
        price_finish = int(row.find("FINISH").text)

        if price_finish > 0:
            price = price_finish
        else:
            price = 0

        kpp = row.find("KPP_TYPE").text
        if kpp == '2':
            kpp = 'Автомат'
        elif kpp == '1':
            kpp = 'Механика'

        engine_volume = float(row.find("ENG_V").text) / 1000

        car = {
            "api_id": row.find("ID").text,
            "brand": row.find("MARKA_NAME").text,
            "model": row.find("MODEL_NAME").text,
            "year": row.find("YEAR").text,
            "color": color_tags_dict[row.find("COLOR").text],
            "transmission": kpp,
            "engine_volume": f"{engine_volume:.2f}"[:-1],
            "drive": priv_tags_dict[row.find("PRIV").text],
            "mileage": row.find("MILEAGE").text,
            "rate": row.find('RATE').text
        }
        try:
            car["price"], car["toll"], car['outside'] = calc_price(
                price=price,
                currency=currency,
                year=int(row.find("YEAR").text),
                volume=int(row.find("ENG_V").text),
                table=table,
                conf=config
            )
        except:
            car["price"] = 0
        car["photos"] = row.find("IMAGES").text.replace("=50", "").split("#")
        list_car.append(car)

    return list_car


def get_count(html_text: str):
    soup = BeautifulSoup(html_text, "lxml-xml")
    root = soup.find("aj")
    rows = root.find("row")
    count = int(rows.find("TAG0").text)
    return count
