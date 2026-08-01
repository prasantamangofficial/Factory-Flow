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


# --- Period selection -------------------------------------------------
#
# The dashboard used to hard-code "this calendar month". On the 1st of a
# month that window is empty, so every KPI read NPR 0 even though the
# database was full. The window is now user-selectable and defaults to a
# rolling 30 days, which never goes blank just because the month rolled.

DEFAULT_PERIOD = "30d"


def _previous_month(today):
    """First and last day of the month before today's month."""
    last_day = today.replace(day=1) - timedelta(days=1)
    return last_day.replace(day=1), last_day


# (key, label for the KPI captions, label for the button, function returning
#  (start, end). Either bound may be None, meaning "unbounded on that side".)
PERIODS = [
    ("30d",  "Last 30 Days",   "30 Days",    lambda today: (today - timedelta(days=29), None)),
    ("prev", "Previous Month", "Prev Month", _previous_month),
    ("year", "This Year",      "This Year",  lambda today: (today.replace(month=1, day=1), None)),
    ("all",  "All Time",       "All Time",   lambda today: (None, None)),
]

_PERIOD_MAP = {key: (label, short, fn) for key, label, short, fn in PERIODS}


def _resolve_period(request):
    """Return (key, label, start, end) for the requested window."""
    key = request.GET.get("period") or DEFAULT_PERIOD
    if key not in _PERIOD_MAP:
        key = DEFAULT_PERIOD

    label, _short, range_fn = _PERIOD_MAP[key]
    start, end = range_fn(date.today())

    # A closed range names itself: "July 2026" beats "Previous Month".
    if start and end:
        label = start.strftime("%B %Y")

    return key, label, start, end


def _in_period(queryset, start, end):
    if start:
        queryset = queryset.filter(date__gte=start)
    if end:
        queryset = queryset.filter(date__lte=end)
    return queryset


@login_required
def dashboard(request):
    period_key, period_label, start, end = _resolve_period(request)

    income_total = _in_period(Income.objects.all(), start, end).aggregate(
        t=Sum("amount"))["t"] or 0

    expense_total = _in_period(Expense.objects.all(), start, end).aggregate(
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
        # period selector
        "period": period_key,
        "period_label": period_label,
        "period_options": [(k, short) for k, _lbl, short, _fn in PERIODS],
        "has_any_data": Income.objects.exists() or Expense.objects.exists(),
    })


@login_required
def dashboard_charts(request):
    period_key, period_label, start, end = _resolve_period(request)

    months = _last_six_months()
    chart_start = months[0]

    def monthly(model):
        rows = (model.objects
                .filter(date__gte=chart_start)
                .annotate(m=TruncMonth("date"))
                .values("m")
                .annotate(total=Sum("amount")))
        return {r["m"].strftime("%Y-%m"): float(r["total"]) for r in rows}

    inc = monthly(Income)
    exp = monthly(Expense)
    keys = [m.strftime("%Y-%m") for m in months]

    breakdown = (_in_period(Expense.objects.all(), start, end)
                 .values("category__name")
                 .annotate(total=Sum("amount"))
                 .order_by("-total"))

    return JsonResponse({
        "labels": [m.strftime("%b") for m in months],
        "income": [inc.get(k, 0) for k in keys],
        "expenses": [exp.get(k, 0) for k in keys],
        "period": period_key,
        "period_label": period_label,
        "breakdown": {
            "labels": [b["category__name"] for b in breakdown],
            "values": [float(b["total"]) for b in breakdown],
        },
    })