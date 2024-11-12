from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Selection)
class SelectionAdmin(admin.ModelAdmin):
    pass
