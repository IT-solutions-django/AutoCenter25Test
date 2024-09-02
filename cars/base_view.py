from django.views.generic.list import BaseListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateResponseMixin
from django.shortcuts import get_list_or_404
import requests
from .forms import FeedbackForm, CarChinaFilterForm
from .paginator import CustomPaginator, get_page
from .get_json_api import get_count, get_car
from .models import UniqueColor


class FilteredCarListView(BaseListView, TemplateResponseMixin):
    template_name = "base/catalog.html"
    context_object_name = "cars"
    paginate_by = 8
    link_url = None
    title = None
    car_link = None
    url_api = None
    url_api_now = 'http://78.46.90.228/api/?ip={ip}&code=A25nhGfE56Kd&sql=select+*+from+{table}+WHERE+1+=+1+and+AUCTION+NOT+LIKE+"%USS%"+and+{default_filter}+{filter}order+by+marka_id+limit+{offset},{limit}'
    url_api_count = 'http://78.46.90.228/api/?ip={ip}&code=A25nhGfE56Kd&sql=select+count(*)+from+{table}+WHERE+1+=+1+and+AUCTION+NOT+LIKE+"%USS%"+and+{default_filter}+{filter}'
    
    
    #table = "china"
    filter = ""
    default_filter_jpn = 'MARKA_NAME+<>+"ISUZU"+and+MARKA_NAME+<>+"HINO"+and+MARKA_NAME+<>+"MITSUOKA"+and+MARKA_NAME+<>+"BIRKIN"+and+MARKA_NAME+<>+"HITACHI"+and+MARKA_NAME+<>+"ISEKI"+and+MARKA_NAME+<>+"KOBELCO"+and+MARKA_NAME+<>+"KOMATSU"+and+MARKA_NAME+<>+"KUBOTA"+and+MARKA_NAME+<>+"SUMITOMO"+and+MARKA_NAME+<>+"TADANO"+and+MARKA_NAME+<>+"WINNEBAGO"+and+MARKA_NAME+<>+"YAMAHA"+and+MARKA_NAME+<>+"YANMAR"+and+MARKA_NAME+<>+"OTHERS"+and+MARKA_NAME+<>+"TRIUMPH"+and+MARKA_NAME+<>+"TCM"+and+MARKA_NAME+<>+"LANCIA"+and+STATUS+=+"Sold"+and+YEAR+>=+2008'
    
    ip = "45.84.177.55"

    def update_sql(self):
        form = self.filter_form()
        self.filter = ""
        if form.is_valid():
            try:
                if form.cleaned_data["brand"]:
                    self.filter += f'and+MARKA_NAME+LIKE+"%{form.cleaned_data["brand"]}%"+'
                    
                if form.cleaned_data["model"]:
                    self.filter += f'and+MODEL_NAME+LIKE+"%{form.cleaned_data["model"]}%"+'
                    
                if form.cleaned_data["color"]:
                    self.filter += (
                        f'and+COLOR+LIKE+"%{form.cleaned_data["color"]}%"+'
                    )
                    
                if form.cleaned_data["mileage_min"]:
                    mileage = int(
                        form.cleaned_data["mileage_min"].replace(" ", "")
                    )
                    self.filter += f"and+MILEAGE+>=+{mileage}+"
                    
                if form.cleaned_data["mileage_max"]:
                    mileage = int(
                        form.cleaned_data["mileage_max"].replace(" ", "")
                    )
                    self.filter += f"and+MILEAGE+<=+{mileage}+"
                    
                if form.cleaned_data["year_min"]:
                    self.filter += (
                        f"and+YEAR+>=+{form.cleaned_data['year_min']}+"
                    )
                    
                if form.cleaned_data["year_max"]:
                    self.filter += (
                        f"and+YEAR+<=+{form.cleaned_data['year_max']}+"
                    )
                if form.cleaned_data["transmission"]:
                    self.filter += f'and+KPP+LIKE+"%{form.cleaned_data["transmission"]}%"+'

                if form.cleaned_data["drive"]:
                    self.filter += (
                        f'and+PRIV+LIKE+"%{form.cleaned_data["drive"]}%"+'
                    )

                if form.cleaned_data["engine_volume_min"]:
                    eng = int(
                        form.cleaned_data["engine_volume_min"].replace(" ", "")
                    )
                    self.filter += f"and+ENG_V+>=+{eng}+"
                    
                if form.cleaned_data["engine_volume_max"]:
                    eng = int(
                        form.cleaned_data["engine_volume_max"].replace(" ", "")
                    )
                    self.filter += f"and+ENG_V+<=+{eng}+"

            except Exception as e:
                print(e)

    def filter_form(self):
        return self.form_filter(self.request.GET or None)

    def count_page(self):
        if self.table == 'stats':
            get_default_filter = self.default_filter_jpn
        else:
            get_default_filter = 'FINISH+>+0+and+YEAR+>=+2008'
    
        total_cars_response = requests.get(
            self.url_api_count.format(
                table=self.table, filter=self.filter, ip=self.ip, default_filter=get_default_filter
            )
        ).text
        return get_count(total_cars_response)
        #return 10

    def get_context_data(self, **kwargs):
        self.update_sql()
        
        if self.table == 'stats':
            get_default_filter = self.default_filter_jpn
        else:
            get_default_filter = 'FINISH+>+0+and+YEAR+>=+2008'


        total_count = self.count_page()
        page_number = int(self.request.GET.get("page", 1))
        paginator = CustomPaginator(
            count=total_count,
            # count=10,
            per_page=self.paginate_by,
            api_url=self.url_api_now,
            table=self.table,
            default_filter=get_default_filter,
            filter=self.filter,
            ip=self.ip,
            page_number=page_number,
        )

        page_number = self.request.GET.get("page", 1)
        page_obj = get_page(paginator=paginator, page_number=page_number)
        
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
        '+and+YEAR+>=+2008'
        '+and+MARKA_NAME+=+"{brand}"'
        #"+and+ENG_V+>=+{eng_v_min}+and+ENG_V+<=+{eng_v_max}"
        "+limit+0,4"
    )
    ip = "45.84.177.55"
    
    country = None
    recommendations = []

    def get_object(self):
        _, path, car_id = self.request.get_full_path().split("/")

        if path == "car_japan":
            table = "stats"
        if path == "car_china":
            table = "china"

        html_text = requests.get(
            self.api_url.format(
                car_id=car_id,
                table=table,
                ip=self.ip,
            )
        ).text
        obj = get_car(html_text, table)[0]
        obj["img"] = obj["photos"]

        recommendations_text = requests.get(
            self.api_url_recommendations.format(
                brand=obj["brand"],
                #eng_v_min=int(obj["engine_volume"]) - 500,
                #eng_v_max=int(obj["engine_volume"]) + 500,
                table=table,
                ip=self.ip,
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
