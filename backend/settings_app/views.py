import json
from datetime import datetime

import django
from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect

from customers.models import Customer
from expenses.models import Expense
from income.models import Income
from production.models import Production
from products.models import Product
from raw_materials.models import RawMaterial, MaterialPurchase
from suppliers.models import Supplier

from .models import FactorySettings
from .forms import CompanyForm, PreferencesForm

VERSION = "1.1.0"

# Everything a backup needs to restore the factory's books.
BACKUP_MODELS = [
    Customer, Supplier, Product, RawMaterial,
    MaterialPurchase, Production, Income, Expense,
]


@login_required
def settings(request):
    """
    Three independent forms share this page. Each submit button carries a
    `form_name`, so only the form that was actually submitted gets bound --
    otherwise saving Company Information would raise validation errors on
    the untouched password fields.
    """
    config = FactorySettings.load()

    company_form = CompanyForm(instance=config)
    prefs_form = PreferencesForm(instance=config)
    password_form = PasswordChangeForm(user=request.user)

    if request.method == "POST":
        which = request.POST.get("form_name")

        if which == "company":
            company_form = CompanyForm(request.POST, instance=config)
            if company_form.is_valid():
                company_form.save()
                messages.success(request, "Company information saved.")
                return redirect("settings")

        elif which == "preferences":
            prefs_form = PreferencesForm(request.POST, instance=config)
            if prefs_form.is_valid():
                prefs_form.save()
                messages.success(request, "Preferences saved.")
                return redirect("settings")

        elif which == "password":
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                # Changing a password rotates the session hash; without this
                # the user is logged out immediately after succeeding.
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed.")
                return redirect("settings")

    return render(request, "settings.html", {
        "company_form": company_form,
        "prefs_form": prefs_form,
        "password_form": password_form,
        "version": VERSION,
        "django_version": django.get_version(),
        "db_engine": django_settings.DATABASES["default"]["ENGINE"].rsplit(".", 1)[-1],
        "record_counts": [
            ("Customers", Customer.objects.count()),
            ("Suppliers", Supplier.objects.count()),
            ("Products", Product.objects.count()),
            ("Raw materials", RawMaterial.objects.count()),
            ("Production runs", Production.objects.count()),
            ("Sales", Income.objects.count()),
            ("Expenses", Expense.objects.count()),
        ],
    })


@login_required
def settings_backup(request):
    """
    Download every business record as a JSON fixture.

    Restorable with:  python manage.py loaddata <file>
    Deliberately not a copy of db.sqlite3 -- that would carry sessions,
    password hashes and admin logs along with your data.
    """
    payload = []
    for model in BACKUP_MODELS:
        payload.extend(json.loads(
            serializers.serialize("json", model.objects.all())
        ))

    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    response = HttpResponse(json.dumps(payload, indent=1),
                            content_type="application/json")
    response["Content-Disposition"] = (
        f'attachment; filename="factoryflow-backup-{stamp}.json"')
    return response