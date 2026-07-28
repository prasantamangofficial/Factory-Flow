from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from dashboard.views import dashboard, dashboard_charts
from income.views import income, income_delete
from expenses.views import expenses, expense_delete
from raw_materials.views import raw_materials, purchase_delete
from suppliers.views import suppliers, supplier_delete
from customers.views import customers, customer_delete
from production.views import production, production_delete
from products.views import products, product_delete
from reports.views import reports
from settings_app.views import settings as settings_view

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", dashboard, name="dashboard"),
    path("api/dashboard-charts/", dashboard_charts, name="dashboard-charts"),

    path("production/", production, name="production"),
    path("products/", products, name="products"),
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

    # Customers
    path("customers/", customers, name="customers"),
    path("customers/<int:pk>/delete/", customer_delete, name="customer_delete"),

    # Products
    path("products/", products, name="products"),
    path("products/<int:pk>/delete/", product_delete, name="product_delete"),

    # Production
    path("production/", production, name="production"),
    path("production/<int:pk>/delete/", production_delete, name="production_delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)