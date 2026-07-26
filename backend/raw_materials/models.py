from django.db import models


class RawMaterial(models.Model):
    name = models.CharField(max_length=120)
    unit = models.CharField(max_length=20, default="kg")
    quantity_in_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reorder_level = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    @property
    def stock_value(self):
        return self.quantity_in_stock * self.unit_cost

    def __str__(self):
        return self.name