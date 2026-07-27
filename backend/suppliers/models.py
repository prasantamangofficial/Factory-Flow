from django.db import models
from django.db.models import Sum


class Supplier(models.Model):
    name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    materials_supplied = models.CharField(max_length=200)
    address = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    @property
    def total_spend(self):
        return self.purchases.aggregate(t=Sum("total_cost"))["t"] or 0

    def __str__(self):
        return self.name