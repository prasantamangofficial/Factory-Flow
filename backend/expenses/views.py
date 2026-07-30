from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from .models import Expense
from .forms import ExpenseForm


def expenses(request):
    edit_id = request.GET.get("edit")
    instance = get_object_or_404(Expense, pk=edit_id) if edit_id else None

    if request.method == "POST":
        post_id = request.POST.get("edit_id")
        instance = get_object_or_404(Expense, pk=post_id) if post_id else None
        form = ExpenseForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("expenses")
    else:
        form = ExpenseForm(instance=instance)

    records = Expense.objects.select_related("category")

    return render(request, "expenses.html", {
        "form": form,
        "editing": instance,
        "expenses": records,
        "total_expenses": records.aggregate(t=Sum("amount"))["t"] or 0,
        "by_category": records.values("category__name").annotate(
            total=Sum("amount")).order_by("-total"),
    })


def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == "POST":
        expense.delete()
    return redirect("expenses")