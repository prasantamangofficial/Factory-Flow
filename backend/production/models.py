from django.db import models


class Production(models.Model):
    MACHINE_CHOICES = [
        ("cutting", "Cutting"),
        ("stitching", "Stitching"),
        ("assembly", "Assembly"),
        ("finishing", "Finishing"),
    ]

    STATUS_CHOICES = [
        ("completed", "Completed"),
        ("running", "Running"),
        ("pending", "Pending"),
    ]

    date = models.DateField()
    batch_no = models.CharField(max_length=30, unique=True)
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="production_runs",
    )
    supervisor = models.CharField(max_length=120)
    machine = models.CharField(max_length=15, choices=MACHINE_CHOICES, default="cutting")
    target_quantity = models.PositiveIntegerField()
    produced_quantity = models.PositiveIntegerField(default=0)
    defective_quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="pending")
    remarks = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-date", "-id"]

    @property
    def good_quantity(self):
        return self.produced_quantity - self.defective_quantity

    @property
    def efficiency(self):
        if not self.target_quantity:
            return 0
        return round((self.good_quantity / self.target_quantity) * 100)

    @property
    def progress(self):
        if not self.target_quantity:
            return 0
        return round((self.produced_quantity / self.target_quantity) * 100)

    def __str__(self):
        return f"{self.batch_no} - {self.product}"