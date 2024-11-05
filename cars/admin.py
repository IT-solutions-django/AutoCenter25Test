from random import randint

from django.contrib import admin
from .models import *


def copy_objects(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.price = randint(1_000_000, 100_000_000)
        object.save()


copy_objects.short_description = "Копировать выбранные объекты"


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    pass


@admin.register(PhotoCars)
class PhotoCarsAdmin(admin.ModelAdmin):
    pass


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass


@admin.register(CarMainPage)
class CarMainPageAdmin(admin.ModelAdmin):
    actions = [copy_objects]


@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    pass


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(ColorTag)
class UniqueColorAdmin(admin.ModelAdmin):
    pass


@admin.register(CarMark)
class UniqueColorAdmin(admin.ModelAdmin):
    pass


@admin.register(CarModel)
class UniqueColorAdmin(admin.ModelAdmin):
    pass


@admin.register(Privod)
class UniqueColorAdmin(admin.ModelAdmin):
    pass


@admin.register(PrivodTag)
class UniqueColorAdmin(admin.ModelAdmin):
    pass


@admin.register(BaseFilter)
class UniqueColorAdmin(admin.ModelAdmin):
    pass
