import json
from datetime import datetime


def get_tof(price: int, cars_tof: list[dict]):
    for interval in cars_tof:
        if (
                interval["price_interval"][0]
                < price
                <= float(interval["price_interval"][1])
        ):
            return interval["tof"]


def get_new_cars_duty(
        price_eur: float, volume: int, currency_eur: float, new_cars_duty: list[dict]
):
    volume = float(volume)

    for duty_info in new_cars_duty:
        if (
                duty_info["price_interval"][0]
                <= price_eur
                < float(duty_info["price_interval"][1])
        ):
            duty = price_eur * duty_info["multiplier"]
            if float(duty) / volume < duty_info["min_by_eng_v"]:
                duty = volume * duty_info["min_by_eng_v"]
            return duty * currency_eur


def get_old_car_duty(
        volume: int, age: int, currency_eur: float, old_cars_duty: list[dict]
):
    for duty_info in old_cars_duty:
        if duty_info["age_interval"][0] <= age < float(
                duty_info["age_interval"][1]
        ) and duty_info["volume_interval"][0] < volume <= float(
            duty_info["volume_interval"][1]
        ):
            duty = volume * duty_info["multiplier"]
            return duty * currency_eur


def get_yts(age: int, volume: int, cars_yts: list[dict]):
    for yts_info in cars_yts:
        if yts_info["age_interval"][0] <= age < float(
                yts_info["age_interval"][1]
        ) and yts_info["volume_interval"][0] < volume <= float(
            yts_info["volume_interval"][1]
        ):
            return yts_info["yts"]


def get_config():
    with open("core/calculating_car_price_config.json") as f:
        conf = json.load(f)
    return conf


def calc_price(price, currency, year, volume, table, conf, commission):
    try:
        price = int(price)
        year = int(year)
        volume = int(volume)

        one_rub_currency = conf["table_settings"][table]["currency"]
        if one_rub_currency == 'jpy':
            one_rub = currency.jpy
        elif one_rub_currency == 'cny':
            one_rub = currency.cny
        else:
            one_rub = currency.krw

        price_rus = round(price * one_rub)
        price_eur = float(price_rus) / currency.eur

        age = datetime.now().year - year

        tof = get_tof(price_rus, conf["car_tof"])

        if age < 3:
            duty = get_new_cars_duty(
                price_eur, volume, currency.eur, conf["new_cars_duty"]
            )
        else:
            duty = get_old_car_duty(volume, age, currency.eur, conf["old_cars_duty"])

        yts = get_yts(age, volume, conf["cars_yts"])

        toll = duty + tof + yts

        sanctions_japan_commission = 0

        if table == "stats" and volume > 1800:
            commission_delivery = commission.japan_sanction_commission
            sanctions_japan_commission = (
                    price_rus / 100 * commission.japan_sanction_percent
            )
        elif table == "korea" and price > 30_000_000:
            commission_delivery = commission.korea_sanction_commission
        else:
            commission_delivery = commission.commission_delivery

        full_commission = (
                commission_delivery * one_rub
                + commission.commission_broker
                + commission.commission_storage
                + commission.commission
                + sanctions_japan_commission
        )

        full_price = toll + price_rus + full_commission
        return round(full_price, 2), (int(duty), int(tof), int(yts))
    except Exception as e:
        print(e)
