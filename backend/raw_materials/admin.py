from django.contrib import admin
from .models import RawMaterial


@admin.register(RawMaterial)
class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "unit", "quantity_in_stock", "unit_cost", "stock_value")
    search_fields = ("name",)