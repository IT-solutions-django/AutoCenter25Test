from .models import CarModel
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(["GET"])
def car_main(request, brand):
    data = CarModel.objects.filter(mark=brand, mark__country='Япония').values_list('name', flat=True).order_by('name')
    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
def car_china(request, brand):
    data = CarModel.objects.filter(mark=brand, mark__country='Китай').values_list('name', flat=True).order_by('name')
    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
def car_korea(request, brand):
    data = CarModel.objects.filter(mark=brand, mark__country='Корея').values_list('name', flat=True).order_by('name')
    return Response(data, status=status.HTTP_200_OK)
