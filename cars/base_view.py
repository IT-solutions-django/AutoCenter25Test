import datetime
from django.views.generic.list import BaseListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateResponseMixin
from django.shortcuts import get_list_or_404
import requests
from .forms import FeedbackForm
from .paginator import CustomPaginator, get_page
from .get_json_api import get_count, get_car
from .models import CarMark, Privod, Color, BaseFilter
from utils.get_user_ip import get_user_ip

ORDERING = {
    "asc_mileage": "ORDER+BY+MILEAGE+ASC+",
    "desc_mileage": "ORDER+BY+MILEAGE+DESC+",
    "asc_price": "ORDER+BY+FINISH+ASC+",
    "desc_price": "ORDER+BY+FINISH+DESC+",
    "asc_eng_v": "ORDER+BY+ENG_V+ASC+",
    "desc_eng_v": "ORDER+BY+ENG_V+DESC+",
    "asc_year": "ORDER+BY+YEAR+ASC+",
    "desc_year": "ORDER+BY+YEAR+DESC+",
    "asc_auc_date": "ORDER+BY+AUCTION_DATE+ASC+",
    "desc_auc_date": "ORDER+BY+AUCTION_DATE+DESC+",
}


def generate_default_filter(country):
    base_filter = BaseFilter.objects.get(country=country)

    excluded_marks = []
    if base_filter.marka_name:
        excluded_marks = base_filter.marka_name.split(',')

    marka_conditions = '+and+'.join(
        [f'MARKA_NAME+<>+"{mark.strip().upper()}"' for mark in excluded_marks]
    )

    if base_filter.kpp_type:
        kpp_types = base_filter.kpp_type.split(',')
        kpp_condition = '+or+'.join([f'KPP_TYPE+=+"{kpp.strip()}"' for kpp in kpp_types])
        kpp_condition = f'({kpp_condition})'
    else:
        kpp_condition = ''

    if base_filter.auction_date:
        max_auction_date = (
                base_filter.auction_date
                and datetime.datetime.now()
                - datetime.timedelta(days=int(base_filter.auction_date))
        ).date()
    else:
        max_auction_date = ''

    if base_filter.rate:
        rate_list = base_filter.rate.split(',')
        rate_join = ','.join(f'"{item}"' for item in rate_list)
        rate = f'({rate_join})'
    else:
        rate = ''

    status_condition = f'STATUS+=+"{base_filter.status}"' if base_filter.status else ''
    year_condition = f'YEAR+>=+{base_filter.year}' if base_filter.year else ''
    engine_volume_condition = f'ENG_V+>+{base_filter.eng_v}+and+ENG_V+<=+{base_filter.max_eng_v * 1000}' if base_filter.eng_v != '' and base_filter.max_eng_v != '' else ''
    mileage_condition = f'MILEAGE+<=+{base_filter.mileage}' if base_filter.mileage else ''
    finish_condition = f'FINISH+>+{base_filter.finish}' if base_filter.finish else ''
    kpp_condition = kpp_condition
    max_auction_date = f"AUCTION_DATE+>=+'{max_auction_date}'" if max_auction_date else ''
    rate = f'RATE+IN+{rate}' if rate else ''

    filter_conditions = "+and+".join(filter(None, [
        marka_conditions,
        status_condition,
        year_condition,
        engine_volume_condition,
        mileage_condition,
        finish_condition,
        kpp_condition,
        max_auction_date,
        rate
    ]))

    return filter_conditions


class FilteredCarListView(BaseListView, TemplateResponseMixin):
    template_name = "base/catalog.html"
    context_object_name = "cars"
    paginate_by = 8
    link_url = None
    title = None
    car_link = None
    url_api = None
    url_api_now = 'http://78.46.90.228/api/?ip={ip}&code=A25nhGfE56Kd&sql=select+*+from+{table}+WHERE+1+=+1+and+AUCTION+NOT+LIKE+"%USS%"+and+{default_filter}+{filter}limit+{offset},{limit}'
    url_api_count = 'http://78.46.90.228/api/?ip={ip}&code=A25nhGfE56Kd&sql=select+count(*)+from+{table}+WHERE+1+=+1+and+AUCTION+NOT+LIKE+"%USS%"+and+{default_filter}+{filter}'

    TRANSMISSION_CHOICES = {
        "": "",
        "2": "Автомат",
        "1": "Механика",
    }

    filter = ""

    def update_sql(self):
        get_params = self.request.GET
        self.filter = ""

        if get_params.get("brand"):
            selected_brand_id = get_params["brand"]
            brand_name = CarMark.objects.get(id=selected_brand_id).name
            self.filter += f'and+MARKA_NAME+=+"{brand_name}"+'
        else:
            brand_name = None

        if get_params.get("model"):
            self.filter += f'and+MODEL_NAME+=+"{get_params["model"]}"+'

        if get_params.get("color"):
            selected_color_id = get_params["color"]
            selected_color = Color.objects.prefetch_related('tags_color').get(id=selected_color_id)
            color_tags = [tag.name for tag in selected_color.tags_color.all()]
            color_tags_str = '","'.join(color_tags)
            self.filter += f'and+COLOR+IN+("{color_tags_str}")+'
        else:
            selected_color = None

        if get_params.get("mileage_min"):
            mileage = int(get_params["mileage_min"].replace(" ", ""))
            self.filter += f"and+MILEAGE+>=+{mileage}+"

        if get_params.get("mileage_max"):
            mileage = int(get_params["mileage_max"].replace(" ", ""))
            self.filter += f"and+MILEAGE+<=+{mileage}+"

        if get_params.get("year_min"):
            self.filter += f"and+YEAR+>=+{get_params['year_min']}+"

        if get_params.get("year_max"):
            self.filter += f"and+YEAR+<=+{get_params['year_max']}+"

        if get_params.get("transmission"):
            selected_kpp_id = get_params["transmission"]
            self.filter += f'and+KPP_TYPE+=+"{selected_kpp_id}"+'
        else:
            selected_kpp_id = ''

        if get_params.get("drive"):
            selected_drive_id = get_params["drive"]
            selected_drive = Privod.objects.get(id=selected_drive_id)

            if selected_drive.name == 'Полный':
                other_drives = Privod.objects.prefetch_related('tags_priv').exclude(id=selected_drive_id)
            else:
                other_drives = Privod.objects.filter(id=selected_drive_id)

            priv_tags = list(
                {tag.name for drive in other_drives for tag in drive.tags_priv.all()})

            if priv_tags:
                priv_tags_str = '","'.join(priv_tags)
                if selected_drive.name == 'Полный':
                    self.filter += f'and+PRIV+NOT+IN+("{priv_tags_str}")+'
                else:
                    self.filter += f'and+PRIV+IN+("{priv_tags_str}")+'
        else:
            selected_drive = None

        if get_params.get("engine_volume_min"):
            eng = int(get_params["engine_volume_min"].replace(" ", ""))
            eng_min_float = f'{eng / 1000: .1f}'
            self.filter += f"and+ENG_V+>=+{eng}+"
        else:
            eng_min_float = ''

        if get_params.get("engine_volume_max"):
            eng = int(get_params["engine_volume_max"].replace(" ", ""))
            eng_max_float = f'{eng / 1000: .1f}'
            self.filter += f"and+ENG_V+<=+{eng}+"
        else:
            eng_max_float = ''

        if get_params.get("rate"):
            self.filter += f'and+RATE+=+"{get_params.get("rate")}"+'

        if get_params.get("ordering"):
            now_ordering = get_params.get("ordering")
            self.filter += ORDERING[now_ordering]
        else:
            now_ordering = ''

        return brand_name, selected_drive, selected_color, selected_kpp_id, eng_min_float, eng_max_float, now_ordering

    def filter_form(self):
        return self.form_filter(self.request.GET or None)

    def count_page(self, get_default_filter):
        ip = get_user_ip(self.request)

        total_cars_response = requests.get(
            self.url_api_count.format(
                table=self.table, filter=self.filter, ip=ip, default_filter=get_default_filter
            )
        ).text
        return get_count(total_cars_response)

    def get_context_data(self, **kwargs):
        ip = get_user_ip(self.request)

        if self.table == 'stats':
            get_default_filter = generate_default_filter("Япония")
            country = "Япония"
        elif self.table == 'main':
            get_default_filter = generate_default_filter("Корея")
            country = "Корея"
        elif self.table == 'china':
            get_default_filter = generate_default_filter("Китай")
            country = "Китай"

        brand, priv, color, kpp, eng_min, eng_max, now_ordering = self.update_sql()

        if priv is not None:
            priv = priv.name

        if color is not None:
            color = color.name

        total_count = self.count_page(get_default_filter)
        page_number = int(self.request.GET.get("page", 1))
        paginator = CustomPaginator(
            count=total_count,
            per_page=self.paginate_by,
            api_url=self.url_api_now,
            table=self.table,
            default_filter=get_default_filter,
            filter=self.filter,
            ip=ip,
            page_number=page_number
        )

        page_number = self.request.GET.get("page", 1)
        page_obj = get_page(paginator=paginator, page_number=page_number)

        ordering_params = [
            ("asc_mileage", "Пробег: по возрастанию"),
            ("desc_mileage", "Пробег: по убыванию"),
            ("asc_price", "Стоимость: по возрастанию"),
            ("desc_price", "Стоимость: по убыванию"),
            ("asc_eng_v", "Объем: по возрастанию"),
            ("desc_eng_v", "Объем: по убыванию"),
            ("asc_year", "Год: по возрастанию"),
            ("desc_year", "Год: по убыванию"),
        ]

        if self.table == "stats":
            ordering_params.extend(
                [
                    ("asc_auc_date", "Дата аукциона: по возрастанию"),
                    ("desc_auc_date", "Дата аукциона: по убыванию"),
                ]
            )

        ordering_params_dict = {key: value for key, value in ordering_params}
        ordering_params_dict[""] = ""

        return {
            "page_obj": page_obj,
            "is_paginated": page_obj.has_other_pages(),
            "cars": page_obj.object_list,
            "filter_form": self.filter_form(),
            "link_url": self.link_url,
            "feedbackForm": FeedbackForm(),
            "title": self.title,
            "car_link": self.car_link,
            "url_api": self.url_api,
            "brand_name": brand,
            "priv": priv,
            "color": color,
            "kpp": self.TRANSMISSION_CHOICES.get(kpp),
            "eng_min": eng_min,
            "eng_max": eng_max,
            "country": country,
            "ordering_params": ordering_params,
            "now_ordering": ordering_params_dict[now_ordering]
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)


class CarDetailView(DetailView):
    template_name = "car.html"
    context_object_name = "car"
    api_url = 'http://78.46.90.228/api/?ip={ip}&code=A25nhGfE56Kd&sql=select+*+from+{table}+WHERE+id+=+"{car_id}"'

    api_url_recommendations = (
        "http://78.46.90.228/api/?ip={ip}&code=A25nhGfE56Kd&sql=select+*+from+{table}"
        '+WHERE+1+=+1+and+AUCTION+NOT+LIKE+"%USS%"'
        '+and+{default_filter}'
        '+and+MARKA_NAME+=+"{brand}"'
        "+limit+0,4"
    )

    country = None
    recommendations = []

    def get_object(self):
        ip = get_user_ip(self.request)

        _, path, car_id = self.request.get_full_path().split("/")

        if path == "car_japan":
            table = "stats"
        if path == "car_china":
            table = "china"
        if path == 'car_korea':
            table = 'main'

        html_text = requests.get(
            self.api_url.format(
                car_id=car_id,
                table=table,
                ip=ip,
            )
        ).text
        obj = get_car(html_text, table)[0]
        obj["img"] = obj["photos"]

        default_filter = generate_default_filter(self.country)

        recommendations_text = requests.get(
            self.api_url_recommendations.format(
                brand=obj["brand"],
                table=table,
                ip=ip,
                default_filter=default_filter
            )
        ).text

        try:
            self.recommendations = get_car(recommendations_text, table)
        except Exception as e:
            self.recommendations = []
            print(e)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedbackForm"] = FeedbackForm()
        context["country"] = self.country
        context["recommendations"] = self.recommendations

        return context


class CarKoreaMainView(DetailView):
    template_name = "car.html"
    context_object_name = "car"

    def get_object(self):
        queryset = self.get_queryset()
        obj_list = get_list_or_404(
            queryset, **{self.slug_field: self.kwargs[self.slug_url_kwarg]}
        )
        obj = obj_list[0]
        obj.img = [i.image.url for i in obj.photos.all()]

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedbackForm"] = FeedbackForm()
        context["country"] = "Корея"
        context["recommendations"] = self.model.objects.order_by("?")[:4]

        return context
