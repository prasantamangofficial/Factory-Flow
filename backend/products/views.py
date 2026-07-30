from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Product
from .forms import ProductForm


@login_required
def products(request):
    edit_id = request.GET.get("edit")
    instance = get_object_or_404(Product, pk=edit_id) if edit_id else None

    if request.method == "POST":
        post_id = request.POST.get("edit_id")
        instance = get_object_or_404(Product, pk=post_id) if post_id else None
        form = ProductForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("products")
    else:
        form = ProductForm(instance=instance)

    items = Product.objects.all()

    return render(request, "products.html", {
        "form": form,
        "editing": instance,
        "products": items,
        "total_products": items.count(),
        "in_stock": sum(1 for p in items if p.stock_status == "ok"),
        "low_stock": sum(1 for p in items if p.stock_status == "low"),
        "out_of_stock": sum(1 for p in items if p.stock_status == "out"),
        "inventory_value": sum(p.stock_value for p in items),
    })


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
    return redirect("products")