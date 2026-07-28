from django import forms
from .models import Production


class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = ["date", "batch_no", "product", "supervisor", "machine",
                  "target_quantity", "produced_quantity", "defective_quantity",
                  "status", "remarks"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "batch_no": forms.TextInput(attrs={"placeholder": "BATCH-001"}),
            "supervisor": forms.TextInput(attrs={"placeholder": "Supervisor name"}),
            "target_quantity": forms.NumberInput(attrs={"placeholder": "500"}),
            "produced_quantity": forms.NumberInput(attrs={"placeholder": "480"}),
            "defective_quantity": forms.NumberInput(attrs={"placeholder": "5"}),
            "remarks": forms.TextInput(attrs={"placeholder": "Production notes"}),
        }

    def clean(self):
        cleaned = super().clean()
        produced = cleaned.get("produced_quantity") or 0
        defective = cleaned.get("defective_quantity") or 0
        if defective > produced:
            raise forms.ValidationError(
                "Defective quantity cannot exceed produced quantity."
            )
        return cleaned