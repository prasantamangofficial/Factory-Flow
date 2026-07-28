from django.db import models
from django.db.models import Sum


class Customer(models.Model):
    TYPE_CHOICES = [
        ("retailer", "Retailer"),
        ("wholesaler", "Wholesaler"),
        ("distributor", "Distributor"),
        ("individual", "Individual"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

    name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=200, blank=True)
    customer_type = models.CharField(max_length=15, choices=TYPE_CHOICES, default="retailer")
    business_name = models.CharField(max_length=150, blank=True)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    remarks = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    @property
    def total_orders(self):
        return self.incomes.count()

    @property
    def total_purchase(self):
        return self.incomes.aggregate(t=Sum("amount"))["t"] or 0

    def __str__(self):
        return self.name