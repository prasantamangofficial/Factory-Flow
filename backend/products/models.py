from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("sports", "Sports Shoes"),
        ("school", "School Shoes"),
        ("casual", "Casual Shoes"),
        ("formal", "Formal Shoes"),
        ("boots", "Boots"),
        ("sandals", "Sandals"),
    ]

    STATUS_CHOICES = [
        ("available", "Available"),
        ("discontinued", "Discontinued"),
    ]

    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=40, unique=True)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES, default="sports")
    brand = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=10, blank=True)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="available")
    description = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ["sku"]

    @property
    def stock_value(self):
        return self.quantity_in_stock * self.selling_price

    @property
    def stock_status(self):
        if self.quantity_in_stock == 0:
            return "out"
        if self.quantity_in_stock <= self.reorder_level:
            return "low"
        return "ok"

    def __str__(self):
        return f"{self.sku} - {self.name}"