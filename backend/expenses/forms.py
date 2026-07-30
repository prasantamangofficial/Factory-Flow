from datetime import date

from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["date", "category", "description", "amount"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.TextInput(attrs={"placeholder": "Expense description"}),
            "amount": forms.NumberInput(attrs={"placeholder": "0", "step": "0.01"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields["date"].initial = date.today()