from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from .models import Income
from .forms import IncomeForm


def income(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("income")
    else:
        form = IncomeForm()

    sales = Income.objects.select_related("customer", "product")

    return render(request, "income.html", {
        "form": form,
        "sales": sales,
        "total_sales": sales.aggregate(t=Sum("amount"))["t"] or 0,
        "paid_total": sales.filter(payment_status="paid").aggregate(t=Sum("amount"))["t"] or 0,
        "pending_total": sales.filter(payment_status="pending").aggregate(t=Sum("amount"))["t"] or 0,
        "invoice_count": sales.count(),
    })


def income_delete(request, pk):
    sale = get_object_or_404(Income, pk=pk)
    if request.method == "POST":
        sale.delete()
    return redirect("income")