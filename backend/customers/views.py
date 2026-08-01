from django.contrib.auth.decorators import login_required
from django.db.models import Q
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

    q = request.GET.get("q", "").strip()
    records = Customer.objects.all()

    if q:
        records = records.filter(
            Q(name__icontains=q)
            | Q(contact_person__icontains=q)
            | Q(phone__icontains=q)
            | Q(email__icontains=q)
            | Q(address__icontains=q)
            | Q(business_name__icontains=q)
        )

    return render(request, "customers.html", {
        "form": form,
        "editing": instance,
        "customers": records,
        "q": q,
    })


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
    return redirect("customers")