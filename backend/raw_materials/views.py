from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import RawMaterial, MaterialPurchase
from .forms import MaterialPurchaseForm


@login_required
def raw_materials(request):
    edit_id = request.GET.get("edit")
    instance = get_object_or_404(MaterialPurchase, pk=edit_id) if edit_id else None

    if request.method == "POST":
        post_id = request.POST.get("edit_id")
        old = get_object_or_404(MaterialPurchase, pk=post_id) if post_id else None

        old_qty = old.quantity if old else 0
        old_material = old.material if old else None

        form = MaterialPurchaseForm(request.POST, instance=old)
        if form.is_valid():
            purchase = form.save()

            if old_material and old_material.pk != purchase.material.pk:
                old_material.quantity_in_stock -= old_qty
                old_material.save()
                old_qty = 0

            material = purchase.material
            material.quantity_in_stock += purchase.quantity - old_qty
            material.unit_cost = purchase.unit_cost
            material.save()

            return redirect("raw_materials")
    else:
        form = MaterialPurchaseForm(instance=instance)

    materials = RawMaterial.objects.all()
    total_value = sum(m.stock_value for m in materials)

    return render(request, "raw_materials.html", {
        "form": form,
        "editing": instance,
        "materials": materials,
        "purchases": MaterialPurchase.objects.select_related("supplier", "material")[:20],
        "total_value": total_value,
    })


@login_required
def purchase_delete(request, pk):
    purchase = get_object_or_404(MaterialPurchase, pk=pk)

    if request.method == "POST":
        material = purchase.material
        material.quantity_in_stock -= purchase.quantity
        material.save()
        purchase.delete()

    return redirect("raw_materials")