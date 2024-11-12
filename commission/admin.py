from django.contrib import admin

from .models import *


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    pass
