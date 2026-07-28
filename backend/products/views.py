from django.shortcuts import render, redirect, get_object_or_404

from .models import Product
from .forms import ProductForm


def products(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("products")
    else:
        form = ProductForm()

    items = Product.objects.all()

    return render(request, "products.html", {
        "form": form,
        "products": items,
        "total_products": items.count(),
        "in_stock": sum(1 for p in items if p.stock_status == "ok"),
        "low_stock": sum(1 for p in items if p.stock_status == "low"),
        "out_of_stock": sum(1 for p in items if p.stock_status == "out"),
        "inventory_value": sum(p.stock_value for p in items),
    })


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
    return redirect("products")