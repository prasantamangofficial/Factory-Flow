from django.shortcuts import render, redirect, get_object_or_404

from .models import Customer
from .forms import CustomerForm


def customers(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("customers")
    else:
        form = CustomerForm()

    return render(request, "customers.html", {
        "form": form,
        "customers": Customer.objects.all(),
    })


def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
    return redirect("customers")