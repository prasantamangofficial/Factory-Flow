from django import forms
from .models import MaterialPurchase


class MaterialPurchaseForm(forms.ModelForm):
    class Meta:
        model = MaterialPurchase
        fields = ["date", "supplier", "material", "quantity", "unit_cost",
                  "payment_status", "remarks"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "quantity": forms.NumberInput(attrs={"placeholder": "0", "step": "0.01"}),
            "unit_cost": forms.NumberInput(attrs={"placeholder": "0", "step": "0.01"}),
            "remarks": forms.TextInput(attrs={"placeholder": "Optional notes"}),
        }