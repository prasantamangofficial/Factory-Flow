from datetime import date

from django import forms
from .models import Income


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["date", "invoice_no", "customer", "channel", "product",
                  "pairs_sold", "unit_price", "payment_status", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "invoice_no": forms.TextInput(attrs={"placeholder": "INV-001"}),
            "pairs_sold": forms.NumberInput(attrs={"placeholder": "0"}),
            "unit_price": forms.NumberInput(attrs={"placeholder": "0", "step": "0.01"}),
            "notes": forms.TextInput(attrs={"placeholder": "Additional notes"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields["date"].initial = date.today()