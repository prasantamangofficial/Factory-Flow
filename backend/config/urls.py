from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from dashboard.views import dashboard, dashboard_charts
from income.views import income, income_delete
from expenses.views import expenses, expense_delete
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
    path("production/", production, name="production"),
    path("products/", products, name="products"),
    path("customers/", customers, name="customers"),
    path("reports/", reports, name="reports"),
    path("settings/", settings_view, name="settings"),

    # Income
    path("income/", income, name="income"),
    path("income/<int:pk>/delete/", income_delete, name="income_delete"),

    # Expenses
    path("expenses/", expenses, name="expenses"),
    path("expenses/<int:pk>/delete/", expense_delete, name="expense_delete"),

    # Raw materials
    path("raw-materials/", raw_materials, name="raw_materials"),
    path("raw-materials/<int:pk>/delete/", purchase_delete, name="purchase_delete"),

    # Suppliers
    path("suppliers/", suppliers, name="suppliers"),
    path("suppliers/<int:pk>/delete/", supplier_delete, name="supplier_delete"),

    path("", dashboard, name="dashboard"),
    path("api/dashboard-charts/", dashboard_charts, name="dashboard-charts"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)