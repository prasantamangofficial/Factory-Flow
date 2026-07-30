from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.shortcuts import render

from income.models import Income
from expenses.models import Expense
from products.models import Product
from raw_materials.models import RawMaterial


def _month_start(d):
    return d.replace(day=1)


def _last_six_months():
    cursor = _month_start(date.today())
    months = []
    for _ in range(6):
        months.append(cursor)
        cursor = _month_start(cursor - timedelta(days=1))
    return list(reversed(months))


@login_required
def dashboard(request):
    month_start = _month_start(date.today())

    income_total = Income.objects.filter(date__gte=month_start).aggregate(
        t=Sum("amount"))["t"] or 0

    expense_total = Expense.objects.filter(date__gte=month_start).aggregate(
        t=Sum("amount"))["t"] or 0

    material_value = sum(m.stock_value for m in RawMaterial.objects.all())

    product_count = Product.objects.aggregate(
        t=Sum("quantity_in_stock"))["t"] or 0

    return render(request, "index.html", {
        "income_total": income_total,
        "expense_total": expense_total,
        "net_profit": income_total - expense_total,
        "material_value": material_value,
        "product_count": product_count,
        "recent_income": Income.objects.select_related("customer")[:5],
        "recent_expenses": Expense.objects.select_related("category")[:5],
    })


@login_required
def dashboard_charts(request):
    months = _last_six_months()
    start = months[0]

    def monthly(model):
        rows = (model.objects
                .filter(date__gte=start)
                .annotate(m=TruncMonth("date"))
                .values("m")
                .annotate(total=Sum("amount")))
        return {r["m"].strftime("%Y-%m"): float(r["total"]) for r in rows}

    inc = monthly(Income)
    exp = monthly(Expense)
    keys = [m.strftime("%Y-%m") for m in months]

    breakdown = (Expense.objects
                 .filter(date__gte=_month_start(date.today()))
                 .values("category__name")
                 .annotate(total=Sum("amount"))
                 .order_by("-total"))

    return JsonResponse({
        "labels": [m.strftime("%b") for m in months],
        "income": [inc.get(k, 0) for k in keys],
        "expenses": [exp.get(k, 0) for k in keys],
        "breakdown": {
            "labels": [b["category__name"] for b in breakdown],
            "values": [float(b["total"]) for b in breakdown],
        },
    })