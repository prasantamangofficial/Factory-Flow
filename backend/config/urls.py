from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from dashboard.views import dashboard
from income.views import income
from expenses.views import expenses
from raw_materials.views import raw_materials, purchase_delete
from production.views import production
from products.views import products
from suppliers.views import suppliers, supplier_delete
from customers.views import customers
from reports.views import reports
from settings_app.views import settings as settings_view

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", dashboard, name="dashboard"),
    path("income/", income, name="income"),
    path("expenses/", expenses, name="expenses"),
    path("production/", production, name="production"),
    path("products/", products, name="products"),
    path("customers/", customers, name="customers"),
    path("reports/", reports, name="reports"),
    path("settings/", settings_view, name="settings"),

    # Raw materials
    path("raw-materials/", raw_materials, name="raw_materials"),
    path("raw-materials/<int:pk>/delete/", purchase_delete, name="purchase_delete"),

    # Suppliers
    path("suppliers/", suppliers, name="suppliers"),
    path("suppliers/<int:pk>/delete/", supplier_delete, name="supplier_delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)