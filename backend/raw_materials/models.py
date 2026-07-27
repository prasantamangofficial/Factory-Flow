from django.db import models


class RawMaterial(models.Model):
    name = models.CharField(max_length=120)
    unit = models.CharField(max_length=20, default="kg")
    quantity_in_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reorder_level = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["name"]

    @property
    def stock_value(self):
        return self.quantity_in_stock * self.unit_cost

    def __str__(self):
        return self.name


class MaterialPurchase(models.Model):
    PAYMENT_CHOICES = [
        ("paid", "Paid"),
        ("pending", "Pending"),
    ]

    date = models.DateField()
    supplier = models.ForeignKey(
        "suppliers.Supplier",
        on_delete=models.PROTECT,
        related_name="purchases",
    )
    material = models.ForeignKey(
        RawMaterial,
        on_delete=models.PROTECT,
        related_name="purchases",
    )
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="pending")
    remarks = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-date", "-id"]

    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.unit_cost
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.material} x {self.quantity}"