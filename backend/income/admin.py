from django.contrib import admin
from .models import Income


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ("date", "invoice_no", "customer", "product",
                    "pairs_sold", "unit_price", "amount", "payment_status")
    list_filter = ("payment_status", "channel", "date")
    search_fields = ("invoice_no", "customer__name", "product__name")