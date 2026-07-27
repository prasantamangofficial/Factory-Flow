from django.db import models


class Income(models.Model):
    CHANNEL_CHOICES = [
        ("wholesale", "Wholesale"),
        ("retail", "Retail Shop"),
        ("online", "Online"),
        ("distributor", "Distributor"),
    ]

    PAYMENT_CHOICES = [
        ("paid", "Paid"),
        ("pending", "Pending"),
        ("partial", "Partial"),
    ]

    date = models.DateField()
    invoice_no = models.CharField(max_length=30, unique=True)
    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.PROTECT,
        related_name="incomes",
    )
    channel = models.CharField(max_length=15, choices=CHANNEL_CHOICES, default="wholesale")
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="sales",
    )
    pairs_sold = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    amount = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="pending")
    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-date", "-id"]

    def save(self, *args, **kwargs):
        self.amount = self.pairs_sold * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_no} - {self.amount}"