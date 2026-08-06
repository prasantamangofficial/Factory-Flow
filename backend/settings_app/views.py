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


@login_required
def settings_restore(request):
    """
    Restore business records from a backup JSON file.

    Guardrails, because this is the most destructive action in the app:
      - only accepts models in BACKUP_MODELS, so a stray fixture can't
        touch users, sessions or admin logs
      - runs inside a transaction, so a partial failure rolls back whole
      - refuses anything that isn't valid JSON in Django's fixture shape
    """
    if request.method != "POST" or "backup_file" not in request.FILES:
        return redirect("settings")

    upload = request.FILES["backup_file"]

    if upload.size > 20 * 1024 * 1024:
        messages.error(request, "That file is larger than 20 MB. Restore refused.")
        return redirect("settings")

    try:
        raw = upload.read().decode("utf-8")
        records = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError):
        messages.error(request, "That file isn't valid JSON. Nothing was changed.")
        return redirect("settings")

    if not isinstance(records, list) or not records:
        messages.error(request, "That file isn't a FactoryFlow backup. Nothing was changed.")
        return redirect("settings")

    allowed = {f"{m._meta.app_label}.{m._meta.model_name}" for m in BACKUP_MODELS}
    found = {r.get("model") for r in records if isinstance(r, dict)}

    if not found or not found.issubset(allowed):
        unexpected = ", ".join(sorted(found - allowed)) or "none recognised"
        messages.error(
            request,
            f"That file contains records this app won't restore ({unexpected}). "
            f"Nothing was changed.")
        return redirect("settings")

    try:
        with transaction.atomic():
            restored = 0
            for obj in serializers.deserialize("json", raw):
                obj.save()
                restored += 1
    except Exception as exc:
        messages.error(
            request,
            f"Restore failed and was rolled back — your data is unchanged. ({exc})")
        return redirect("settings")

    messages.success(request, f"Restored {restored} records from {upload.name}.")
    return redirect("settings")