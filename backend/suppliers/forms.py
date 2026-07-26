from django import forms
from .models import Supplier


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "contact_person", "phone", "materials_supplied", "address"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Balaju Leather Co."}),
            "contact_person": forms.TextInput(attrs={"placeholder": "e.g. Ramesh Thapa"}),
            "phone": forms.TextInput(attrs={"placeholder": "e.g. 98510XXXXX"}),
            "materials_supplied": forms.TextInput(attrs={"placeholder": "e.g. Leather, Rubber Soles"}),
            "address": forms.TextInput(attrs={"placeholder": "e.g. Balaju, Kathmandu"}),
        }