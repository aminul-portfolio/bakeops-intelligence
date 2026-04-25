from decimal import Decimal

from django.db import models

from .workspace import Workspace


class Supplier(models.Model):
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="suppliers",
    )
    name = models.CharField(max_length=120)
    contact_name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    lead_time_days = models.PositiveIntegerField(default=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        unique_together = [["workspace", "name"]]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    UNIT_GRAM = "g"
    UNIT_KG = "kg"
    UNIT_ML = "ml"
    UNIT_LITRE = "l"
    UNIT_EACH = "each"

    UNIT_CHOICES = [
        (UNIT_GRAM, "Gram"),
        (UNIT_KG, "Kilogram"),
        (UNIT_ML, "Millilitre"),
        (UNIT_LITRE, "Litre"),
        (UNIT_EACH, "Each"),
    ]

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="ingredients",
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ingredients",
    )
    name = models.CharField(max_length=120)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default=UNIT_GRAM)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal("0.0000"))
    current_stock_quantity = models.DecimalField(max_digits=12, decimal_places=3, default=Decimal("0.000"))
    reorder_level_quantity = models.DecimalField(max_digits=12, decimal_places=3, default=Decimal("0.000"))
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        unique_together = [["workspace", "name"]]

    def __str__(self):
        return self.name


class IngredientLot(models.Model):
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="ingredient_lots",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="lots",
    )
    lot_code = models.CharField(max_length=80)
    received_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    quantity_received = models.DecimalField(max_digits=12, decimal_places=3)
    quantity_remaining = models.DecimalField(max_digits=12, decimal_places=3)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        ordering = ["expiry_date", "ingredient"]
        unique_together = [["workspace", "lot_code"]]

    def __str__(self):
        return f"{self.ingredient} — {self.lot_code}"