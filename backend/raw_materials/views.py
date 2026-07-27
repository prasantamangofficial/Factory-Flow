from django.shortcuts import render, redirect, get_object_or_404

from .models import RawMaterial, MaterialPurchase
from .forms import MaterialPurchaseForm


def raw_materials(request):
    if request.method == "POST":
        form = MaterialPurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save()

            material = purchase.material
            material.quantity_in_stock += purchase.quantity
            material.unit_cost = purchase.unit_cost
            material.save()

            return redirect("raw_materials")
    else:
        form = MaterialPurchaseForm()

    materials = RawMaterial.objects.all()
    total_value = sum(m.stock_value for m in materials)

    return render(request, "raw_materials.html", {
        "form": form,
        "materials": materials,
        "purchases": MaterialPurchase.objects.select_related("supplier", "material")[:20],
        "total_value": total_value,
    })


def purchase_delete(request, pk):
    purchase = get_object_or_404(MaterialPurchase, pk=pk)

    if request.method == "POST":
        material = purchase.material
        material.quantity_in_stock -= purchase.quantity
        material.save()
        purchase.delete()

    return redirect("raw_materials")