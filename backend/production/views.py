from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from .models import Production
from .forms import ProductionForm


@login_required
def production(request):
    edit_id = request.GET.get("edit")
    instance = get_object_or_404(Production, pk=edit_id) if edit_id else None

    if request.method == "POST":
        post_id = request.POST.get("edit_id")
        old = get_object_or_404(Production, pk=post_id) if post_id else None

        old_good = old.good_quantity if old and old.status == "completed" else 0
        old_product = old.product if old else None

        form = ProductionForm(request.POST, instance=old)
        if form.is_valid():
            run = form.save()

            if old_product and old_product.pk != run.product.pk and old_good:
                old_product.quantity_in_stock = max(
                    0, old_product.quantity_in_stock - old_good)
                old_product.save()
                old_good = 0

            new_good = run.good_quantity if run.status == "completed" else 0
            diff = new_good - old_good

            if diff:
                product = run.product
                product.quantity_in_stock = max(0, product.quantity_in_stock + diff)
                product.save()

            return redirect("production")
    else:
        form = ProductionForm(instance=instance)

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
        "editing": instance,
        "runs": runs[:20],
        "today_produced": produced_since(today),
        "week_produced": produced_since(week_start),
        "month_produced": month_produced,
        "month_defective": month_defective,
        "efficiency": efficiency,
    })


@login_required
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