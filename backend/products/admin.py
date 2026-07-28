from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "category", "selling_price",
                    "quantity_in_stock", "status")
    list_filter = ("category", "status")
    search_fields = ("name", "sku")