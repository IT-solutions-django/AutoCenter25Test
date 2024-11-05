import requests
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import logging
from cars.models import (
    Privod,
    PrivodTag
)

URL_COUNTRY = {
    'URL_CHINA': 'http://78.46.90.228/api/?ip=45.84.177.55&code=A25nhGfE56Kd&sql=select+distinct+PRIV+from+china+WHERE+1+=+1+and+AUCTION+NOT+LIKE+"%USS%"+and+YEAR+>=+2008+limit+{},25',
    'URL_JAPAN': 'http://78.46.90.228/api/?ip=45.84.177.55&code=A25nhGfE56Kd&sql=select+distinct+PRIV+from+stats+WHERE+1+=+1+and+AUCTION+NOT+LIKE+"%USS%"+and+YEAR+>=+2008+limit+{},25'
}


def fetch(url):
    response = requests.get(url)
    response.encoding = "windows-1251"
    return response.text


def get_car(url, page=1):
    perpage = (page - 1) * 25

    response_text = fetch(url.format(perpage))

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

            privod = row.find('PRIV')

            elements = {
                "PRIV": privod
            }
            print(elements)

            for key, value in elements.items():
                if value is not None:
                    logging.debug(f"{key}: {value.text}")
                else:
                    logging.debug(f"{key}: None")

            if not all([privod]):
                logging.error(f"Missing essential element in row: {row}")
                continue

            privod = privod.text

            if privod:
                if privod in ('RR', 'MR', 'MIDSHIP', 'FR'):
                    priv, _ = Privod.objects.get_or_create(name="Задний")
                    priv_tag, _ = PrivodTag.objects.get_or_create(name=privod, privod=priv)
                elif privod == 'FF':
                    priv, _ = Privod.objects.get_or_create(name="Передний")
                    priv_tag, _ = PrivodTag.objects.get_or_create(name=privod, privod=priv)
                else:
                    priv, _ = Privod.objects.get_or_create(name="Полный")
                    priv_tag, _ = PrivodTag.objects.get_or_create(name=privod, privod=priv)
            else:
                priv, _ = Privod.objects.get_or_create(name="Полный")
                priv_tag, _ = PrivodTag.objects.get_or_create(name='', privod=priv)

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
        for country in URL_COUNTRY:
            page = 1
            while True:
                rows = get_car(page=page, url=URL_COUNTRY[country])
                if not rows:
                    print("Загрузка завершена!")
                    break
                page += 1
