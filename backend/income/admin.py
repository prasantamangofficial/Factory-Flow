from django.contrib import admin
from .models import Income


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ("invoice_no", "customer", "date", "amount")
    list_filter = ("date",)
    search_fields = ("invoice_no",)