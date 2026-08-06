from django.db import models


class FactorySettings(models.Model):
    """
    Site-wide configuration.

    A singleton: exactly one row, always pk=1. save() forces the id and
    load() fetches it (creating it on first use), so the rest of the app
    never has to check whether a settings row exists.
    """

    CURRENCY_CHOICES = [
        ("NPR", "Nepalese Rupee (NPR)"),
        ("INR", "Indian Rupee (INR)"),
        ("USD", "US Dollar (USD)"),
    ]

    DATE_FORMAT_CHOICES = [
        ("d M Y", "DD Mon YYYY  (06 Aug 2026)"),
        ("d/m/Y", "DD/MM/YYYY   (06/08/2026)"),
        ("m/d/Y", "MM/DD/YYYY   (08/06/2026)"),
        ("Y-m-d", "YYYY-MM-DD   (2026-08-06)"),
    ]

    # --- Company information ---
    factory_name = models.CharField(max_length=150, default="FactoryFlow Industries")
    owner_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    website = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=300, blank=True)
    vat_number = models.CharField(max_length=50, blank=True)

    # --- Preferences ---
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="NPR")
    date_format = models.CharField(max_length=10, choices=DATE_FORMAT_CHOICES, default="d M Y")
    invoice_prefix = models.CharField(max_length=10, default="INV-", blank=True)
    batch_prefix = models.CharField(max_length=10, default="BATCH-", blank=True)
    default_tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=13)
    low_stock_alerts = models.BooleanField(default=True)
    auto_logout_minutes = models.PositiveIntegerField(
        default=30,
        help_text="Minutes of inactivity before logout. 0 disables auto-logout.",
    )

    class Meta:
        verbose_name = "Factory settings"
        verbose_name_plural = "Factory settings"

    def save(self, *args, **kwargs):
        self.pk = 1                      # there can be only one
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass                             # refuse deletion; the app needs a row

    @classmethod
    def load(cls):
        """Fetch the settings row, creating it with defaults on first use."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.factory_name