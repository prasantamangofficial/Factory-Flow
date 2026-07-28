from django.contrib import admin
from .models import Production


@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = ("date", "batch_no", "product", "supervisor",
                    "target_quantity", "produced_quantity",
                    "defective_quantity", "status")
    list_filter = ("status", "machine", "date")
    search_fields = ("batch_no", "supervisor", "product__name")