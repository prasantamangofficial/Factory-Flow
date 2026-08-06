from django import forms

from .models import FactorySettings


class CompanyForm(forms.ModelForm):
    class Meta:
        model = FactorySettings
        fields = ["factory_name", "owner_name", "email", "phone",
                  "website", "address", "vat_number"]
        widgets = {
            "website": forms.TextInput(attrs={"placeholder": "www.factoryflow.com"}),
            "address": forms.TextInput(attrs={"placeholder": "Kathmandu, Nepal"}),
            "phone": forms.TextInput(attrs={"placeholder": "+977-98XXXXXXXX"}),
            "vat_number": forms.TextInput(attrs={"placeholder": "Enter VAT number"}),
        }


class PreferencesForm(forms.ModelForm):
    class Meta:
        model = FactorySettings
        fields = ["currency", "date_format", "invoice_prefix", "batch_prefix",
                  "default_tax_percent", "low_stock_alerts", "auto_logout_minutes"]
        widgets = {
            "default_tax_percent": forms.NumberInput(attrs={"step": "0.01"}),
            "auto_logout_minutes": forms.NumberInput(attrs={"min": "0"}),
        }
        labels = {
            "default_tax_percent": "Default Tax (%)",
            "low_stock_alerts": "Show low-stock warnings",
            "auto_logout_minutes": "Auto logout after (minutes, 0 = never)",
        }