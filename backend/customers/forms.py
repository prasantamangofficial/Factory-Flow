from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "contact_person", "phone", "email", "address",
                  "customer_type", "business_name", "credit_limit",
                  "status", "remarks"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. ABC Shoe Store"}),
            "contact_person": forms.TextInput(attrs={"placeholder": "e.g. Ram Bahadur"}),
            "phone": forms.TextInput(attrs={"placeholder": "+977-98XXXXXXXX"}),
            "email": forms.EmailInput(attrs={"placeholder": "customer@email.com"}),
            "address": forms.TextInput(attrs={"placeholder": "Kathmandu, Nepal"}),
            "business_name": forms.TextInput(attrs={"placeholder": "Optional"}),
            "credit_limit": forms.NumberInput(attrs={"placeholder": "0", "step": "0.01"}),
            "remarks": forms.TextInput(attrs={"placeholder": "Optional notes"}),
        }