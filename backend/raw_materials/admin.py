from django.contrib import admin
from .models import RawMaterial, MaterialPurchase


@admin.register(RawMaterial)
class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "unit", "quantity_in_stock", "unit_cost", "stock_value")
    search_fields = ("name",)


@admin.register(MaterialPurchase)
class MaterialPurchaseAdmin(admin.ModelAdmin):
    list_display = ("date", "supplier", "material", "quantity", "unit_cost", "total_cost")
    list_filter = ("payment_status", "date", "supplier")
    search_fields = ("material__name", "supplier__name")