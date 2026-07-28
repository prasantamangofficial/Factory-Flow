from datetime import date, timedelta

from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from .models import Production
from .forms import ProductionForm


def production(request):
    if request.method == "POST":
        form = ProductionForm(request.POST)
        if form.is_valid():
            run = form.save()

            if run.status == "completed":
                product = run.product
                product.quantity_in_stock += run.good_quantity
                product.save()

            return redirect("production")
    else:
        form = ProductionForm()

    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)

    runs = Production.objects.select_related("product")

    def produced_since(start):
        return runs.filter(date__gte=start).aggregate(
            t=Sum("produced_quantity"))["t"] or 0

    month_runs = runs.filter(date__gte=month_start)
    month_produced = produced_since(month_start)
    month_defective = month_runs.aggregate(t=Sum("defective_quantity"))["t"] or 0
    month_target = month_runs.aggregate(t=Sum("target_quantity"))["t"] or 0

    efficiency = 0
    if month_target:
        efficiency = round(((month_produced - month_defective) / month_target) * 100)

    return render(request, "production.html", {
        "form": form,
        "runs": runs[:20],
        "today_produced": produced_since(today),
        "week_produced": produced_since(week_start),
        "month_produced": month_produced,
        "month_defective": month_defective,
        "efficiency": efficiency,
    })


def production_delete(request, pk):
    run = get_object_or_404(Production, pk=pk)

    if request.method == "POST":
        if run.status == "completed":
            product = run.product
            product.quantity_in_stock = max(
                0, product.quantity_in_stock - run.good_quantity)
            product.save()
        run.delete()

    return redirect("production")