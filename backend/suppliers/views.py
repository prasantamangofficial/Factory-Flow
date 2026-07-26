from django.shortcuts import render, redirect, get_object_or_404

from .models import Supplier
from .forms import SupplierForm


def suppliers(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("suppliers")
    else:
        form = SupplierForm()

    return render(request, "suppliers.html", {
        "form": form,
        "suppliers": Supplier.objects.all(),
    })


def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        supplier.delete()
    return redirect("suppliers")