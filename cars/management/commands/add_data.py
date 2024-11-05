import requests
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import logging
from cars.models import (
    CarMark,
    CarModel
)
from cars.base_view import generate_default_filter

URL = 'http://78.46.90.228/api/?ip=45.84.177.55&code=A25nhGfE56Kd&sql=select+distinct+MARKA_NAME,MODEL_NAME+from+{}+WHERE+1+=+1+and+AUCTION+NOT+LIKE+"%USS%"+and+{}+limit+{},25'


def fetch(url):
    response = requests.get(url)
    response.encoding = "windows-1251"
    return response.text


def get_car(table="", page=1):
    if table == 'china':
        country = 'Китай'
    elif table == 'main':
        country = 'Корея'
    else:
        country = 'Япония'

    perpage = (page - 1) * 25

    default_filter = generate_default_filter(country)

    url = URL.format(table, default_filter, perpage)

    response_text = fetch(url)

    try:
        soup = BeautifulSoup(response_text, "lxml-xml")
        root = soup.find("aj")
        rows = root.find_all("row")
    except Exception as e:
        logging.error(f"Error parsing XML: {e}")
        logging.debug(f"Response text: {response_text}")
        return []

    for row in rows:
        try:
            logging.debug(f"Processing row: {row}")

            brand_element = row.find("MARKA_NAME")
            model_element = row.find("MODEL_NAME")

            elements = {
                "MARKA_NAME": brand_element,
                "MODEL_NAME": model_element,
            }

            for key, value in elements.items():
                if value is not None:
                    logging.debug(f"{key}: {value.text}")
                else:
                    logging.debug(f"{key}: None")

            if not all([brand_element, model_element]):
                logging.error(f"Missing essential element in row: {row}")
                continue

            brand = brand_element.text
            model = model_element.text

            car_mark, _ = CarMark.objects.get_or_create(name=brand, country=country)
            car_model, _ = CarModel.objects.get_or_create(name=model, mark=car_mark)

        except Exception as e:
            logging.error(f"Error processing row: {e}")
            logging.debug(f"Row data: {row}")
            logging.debug(
                f"Row contents: {[(child.name, child.text) for child in list(row) if hasattr(child, 'name') and child.name is not None]}"
            )

    return rows


class Command(BaseCommand):
    help = "Добавляет данные с API"

    def handle(self, *args, **kwargs):
        for table in ('stats', 'main', 'china'):
            page = 1
            while True:
                rows = get_car(table=table, page=page)
                if not rows:
                    print("Загрузка завершена!")
                    break
                page += 1
