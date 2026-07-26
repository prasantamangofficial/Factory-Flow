from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    materials_supplied = models.CharField(max_length=200)
    address = models.CharField(max_length=200, blank=True)
    total_spend = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name