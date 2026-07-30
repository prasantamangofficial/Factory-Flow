from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from .models import Income
from .forms import IncomeForm


@login_required
def income(request):
    edit_id = request.GET.get("edit")
    instance = get_object_or_404(Income, pk=edit_id) if edit_id else None

    if request.method == "POST":
        post_id = request.POST.get("edit_id")
        instance = get_object_or_404(Income, pk=post_id) if post_id else None
        form = IncomeForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("income")
    else:
        form = IncomeForm(instance=instance)

    sales = Income.objects.select_related("customer", "product")

    return render(request, "income.html", {
        "form": form,
        "editing": instance,
        "sales": sales,
        "total_sales": sales.aggregate(t=Sum("amount"))["t"] or 0,
        "paid_total": sales.filter(payment_status="paid").aggregate(t=Sum("amount"))["t"] or 0,
        "pending_total": sales.filter(payment_status="pending").aggregate(t=Sum("amount"))["t"] or 0,
        "invoice_count": sales.count(),
    })


@login_required
def income_delete(request, pk):
    sale = get_object_or_404(Income, pk=pk)
    if request.method == "POST":
        sale.delete()
    return redirect("income")