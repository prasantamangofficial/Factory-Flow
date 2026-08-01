from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .models import Supplier
from .forms import SupplierForm


@login_required
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

    q = request.GET.get("q", "").strip()
    records = Supplier.objects.all()

    if q:
        records = records.filter(
            Q(name__icontains=q)
            | Q(contact_person__icontains=q)
            | Q(phone__icontains=q)
            | Q(materials_supplied__icontains=q)
            | Q(address__icontains=q)
        )

    return render(request, "suppliers.html", {
        "form": form,
        "editing": instance,
        "suppliers": records,
        "q": q,
    })


@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        supplier.delete()
    return redirect("suppliers")