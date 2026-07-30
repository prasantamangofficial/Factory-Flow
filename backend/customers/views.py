from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Customer
from .forms import CustomerForm


@login_required
def customers(request):
    edit_id = request.GET.get("edit")
    instance = get_object_or_404(Customer, pk=edit_id) if edit_id else None

    if request.method == "POST":
        post_id = request.POST.get("edit_id")
        instance = get_object_or_404(Customer, pk=post_id) if post_id else None
        form = CustomerForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("customers")
    else:
        form = CustomerForm(instance=instance)

    return render(request, "customers.html", {
        "form": form,
        "editing": instance,
        "customers": Customer.objects.all(),
    })


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
    return redirect("customers")