from django.shortcuts import render, redirect, get_object_or_404

from .models import Supplier
from .forms import SupplierForm


def suppliers(request):
    edit_id = request.GET.get("edit")
    instance = get_object_or_404(Supplier, pk=edit_id) if edit_id else None

    if request.method == "POST":
        post_id = request.POST.get("edit_id")
        instance = get_object_or_404(Supplier, pk=post_id) if post_id else None
        form = SupplierForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("suppliers")
    else:
        form = SupplierForm(instance=instance)

    return render(request, "suppliers.html", {
        "form": form,
        "editing": instance,
        "suppliers": Supplier.objects.all(),
    })


def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        supplier.delete()
    return redirect("suppliers")