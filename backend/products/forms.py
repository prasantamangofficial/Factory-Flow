from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "sku", "category", "brand", "color", "size",
                  "cost_price", "selling_price", "quantity_in_stock",
                  "reorder_level", "status", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Men Sports Shoes"}),
            "sku": forms.TextInput(attrs={"placeholder": "SKU-1001"}),
            "brand": forms.TextInput(attrs={"placeholder": "FactoryFlow Brand"}),
            "color": forms.TextInput(attrs={"placeholder": "White"}),
            "size": forms.TextInput(attrs={"placeholder": "40"}),
            "cost_price": forms.NumberInput(attrs={"placeholder": "1500", "step": "0.01"}),
            "selling_price": forms.NumberInput(attrs={"placeholder": "2500", "step": "0.01"}),
            "quantity_in_stock": forms.NumberInput(attrs={"placeholder": "250"}),
            "reorder_level": forms.NumberInput(attrs={"placeholder": "50"}),
            "description": forms.TextInput(attrs={"placeholder": "Short product description"}),
        }