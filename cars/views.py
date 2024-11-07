from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from requests import get
from .models import *
from .base_view import (
    FilteredCarListView,
    CarDetailView,
    CarKoreaMainView, generate_default_filter,
)
from .forms import *
import asyncio
from django.views.decorators.http import require_GET
from cars.currency import start_process
from cars.get_json_api import get_car
from utils.get_user_ip import get_user_ip

asyncio.run(start_process())


@require_GET
def robots_txt(request):
    lines = []
    with open("robots.txt") as robots:
        lines.extend(robots.readlines())
    lines = [i.strip() for i in lines]

    return HttpResponse("\n".join(lines), content_type="text/plain")


@require_GET
def sitemap(request):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '   <!--	created with www.mysitemapgenerator.com	-->',
        '   <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '<url>',
        '    <loc>https://autocenter25.com/</loc>',
        '    <lastmod>2024-07-08T15:00:18+01:00</lastmod>',
        '    <priority>1.0</priority>',
        '</url>',
        '<url>',
        '    <loc>https://autocenter25.com/cars_japan/</loc>',
        '    <lastmod>2024-07-08T15:00:18+01:00</lastmod>',
        '    <priority>0.8</priority>',
        '</url>',
        '<url>',
        '    <loc>https://autocenter25.com/cars_china/</loc>',
        '    <lastmod>2024-07-08T15:00:18+01:00</lastmod>',
        '    <priority>0.8</priority>',
        '</url>',
        '<url>',
        '    <loc>https://autocenter25.com/cars_korea/</loc>',
        '    <lastmod>2024-07-08T15:00:18+01:00</lastmod>',
        '    <priority>0.8</priority>',
        '</url>',
        '<url>',
        '    <loc>https://autocenter25.com/cars/1</loc>',
        '    <lastmod>2024-07-08T15:00:18+01:00</lastmod>',
        '    <priority>0.8</priority>',
        '</url>',
        '<url>',
        '    <loc>https://autocenter25.com/cars/2</loc>',
        '    <lastmod>2024-07-08T15:00:18+01:00</lastmod>',
        '    <priority>0.8</priority>',
        '</url>',
        '<url>',
        '    <loc>https://autocenter25.com/cars/3</loc>',
        '    <lastmod>2024-07-08T15:00:18+01:00</lastmod>',
        '    <priority>0.8</priority>',
        '</url>',
        '<url>',
        '    <loc>https://autocenter25.com/cars/4</loc>',
        '    <lastmod>2024-07-08T15:00:18+01:00</lastmod>',
        '    <priority>0.8</priority>',
        '</url>',
        '<url>',
        '    <loc>https://autocenter25.com/cars/5</loc>',
        '    <lastmod>2024-07-08T15:00:18+01:00</lastmod>',
        '    <priority>0.8</priority>',
        '</url>',
        '<url>',
        '    <loc>https://autocenter25.com/cars/6</loc>',
        '    <lastmod>2024-07-08T15:00:18+01:00</lastmod>',
        '    <priority>0.8</priority>',
        '</url>',
        '<url>',
        '    <loc>https://autocenter25.com/cars/7</loc>',
        '    <lastmod>2024-07-08T15:00:18+01:00</lastmod>',
        '    <priority>0.8</priority>',
        '</url>',
        '<url>',
        '    <loc>https://autocenter25.com/cars/8</loc>',
        '    <lastmod>2024-07-08T15:00:18+01:00</lastmod>',
        '    <priority>0.8</priority>',
        '</url>',
        '<url>',
        '    <loc>https://autocenter25.com/article/1</loc>',
        '    <lastmod>2024-07-08T15:00:18+01:00</lastmod>',
        '    <priority>0.8</priority>',
        '</url>',
        '<url>',
        '    <loc>https://autocenter25.com/article/2</loc>',
        '    <lastmod>2024-07-08T15:00:18+01:00</lastmod>',
        '    <priority>0.8</priority>',
        '</url>',
        '</urlset>',
    ]

    return HttpResponse("\n".join(lines), content_type="text/plain")


def main(request):
    ip = get_user_ip(request)
    api_url = 'http://78.46.90.228/api/?ip={ip}&code=A25nhGfE56Kd&sql=select+*+from+{table}+WHERE+1+=+1+and+AUCTION+NOT+LIKE+"%USS%"+and+{default_filter}+{filter}limit+{offset},{limit}'
    url = api_url.format(
        table='stats',
        filter='',
        default_filter=generate_default_filter('Япония'),
        limit=4,
        offset=0,
        ip=ip,
    )
    res_text = get(url).text
    cars = get_car(res_text, 'stats')

    data = {"feedbackForm": FeedbackForm(), "cars": cars,
            "reviews": Reviews.objects.all()}
    return render(request, "main/index.html", data)


def about_us(request):
    data = {"feedbackForm": FeedbackForm()}
    return render(request, "main/about_us.html", data)


def additional_services(request):
    data = {"feedbackForm": FeedbackForm(), "reviews": Reviews.objects.all()}
    return render(request, "main/additional_services.html", data)


def article_1(request):
    return render(request, "main/articles_1.html")


def article_2(request):
    return render(request, "main/articles_2.html")


def article_3(request):
    return render(request, "main/articles_3.html")


@csrf_exempt
def sendFeedBack(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            f = FeedBack(
                name=form.cleaned_data["name"],
                number=form.cleaned_data["number"],
                message=form.cleaned_data["message"],
            )
            f.save()
            name = form.cleaned_data["name"]
            number = form.cleaned_data["number"]
            message = form.cleaned_data["message"]
            get(
                "https://api.telegram.org/bot7308037244:AAEphpg72xfYk_MdRZ1EzuGZQq6i2FuTmDw/sendmessage?chat_id={user_id}&text={text}".format(
                    text=f"Имя: {name}\nТелефон: {number}\nЗапрос: {message}",
                    user_id=629793380,
                )
            )
            get(
                "https://api.telegram.org/bot7308037244:AAEphpg72xfYk_MdRZ1EzuGZQq6i2FuTmDw/sendmessage?chat_id={user_id}&text={text}".format(
                    text=f"Имя: {name}\nТелефон: {number}\nЗапрос: {message}",
                    user_id=6600969548,
                )
            )
            get(
                "https://autocenter.bitrix24.ru/rest/1/5gyn8c68hatc27yv/crm.lead.add.json" \
                "?FIELDS[NAME]={name}"
                "&FIELDS[PHONE][0][VALUE]={number}"
                "&FIELDS[TITLE]=Увидомление%20с%20сайта"
                "&FIELDS[COMMENTS]={message}".format(
                    name=name,
                    number=number,
                    message=message,
                )
            )
    return HttpResponse("Заявка отправлена! Мы скоро перезвоним вам")


class CarsChina(FilteredCarListView):
    form_filter = CarChinaFilterForm
    link_url = "car_list_china"
    title = "Каталог авто из Китая"
    car_link = "car_china"
    table = "china"
    url_api = "/api/cars/china/"


class CarsKorea(FilteredCarListView):
    form_filter = CarKoreaFilterForm
    link_url = "car_list_korea"
    title = "Каталог авто из Кореи"
    car_link = "car_korea"
    url_api = "/api/cars/korea/"
    table = 'main'


class CarsJapan(FilteredCarListView):
    form_filter = CarJapanFilterForm
    link_url = "car_list_japan"
    title = "Каталог авто из Японии"
    table = "stats"
    car_link = "car_japan"
    url_api = "/api/cars/japan/"


class CarMainDetailView(CarKoreaMainView):
    model = CarMainPage
    slug_field = "pk"
    slug_url_kwarg = "pk"


class CarChinaDetailView(CarDetailView):
    slug_field = "api_id"
    slug_url_kwarg = "api_id"
    country = "Китай"


class CarJapanDetailView(CarDetailView):
    slug_field = "api_id"
    slug_url_kwarg = "api_id"
    country = "Япония"


class CarKoreaDetailView(CarDetailView):
    slug_field = "api_id"
    slug_url_kwarg = "api_id"
    country = "Корея"
