import requests
from django.core.management import BaseCommand
from cars.models import Currency


def update_currency_rate():
    url = 'http://auc.autocenter25.com/currency'

    try:
        response = requests.get(url).json()
        currency, _ = Currency.objects.get_or_create(id=0)
        currency.date = response.get("date")
        currency.usd = response.get("usd")
        currency.eur = response.get("eur")
        currency.jpy = response.get("jpy") / 100
        currency.krw = response.get("krw") / 1000
        currency.cny = response.get("cny")
        currency.save()
    except Exception as e:
        print("Что-то не так с парсингом валют")
        print(e)


class Command(BaseCommand):
    help = "Добавляет данные с API"

    def handle(self, *args, **kwargs):
        update_currency_rate()
        print("Загрузка завершена!")
