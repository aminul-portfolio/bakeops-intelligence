from decimal import Decimal

from django.db import models

from .ingredients import Ingredient
from .orders import BakeryOrderItem
from .workspace import StaffMember, Workspace


class Recipe(models.Model):
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    cake = models.ForeignKey(
        "cakes.Cake",
        on_delete=models.CASCADE,
        related_name="bakeops_recipes",
    )
    variant = models.ForeignKey(
        "cakes.CakeVariant",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bakeops_recipes",
    )
    name = models.CharField(max_length=140)
    expected_yield_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("1.00"))
    labour_minutes = models.PositiveIntegerField(default=0)
    overhead_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["cake", "name"]
        unique_together = [["workspace", "cake", "variant", "name"]]

    def __str__(self):
        return self.name


class RecipeLine(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="lines",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name="recipe_lines",
    )
    quantity_required = models.DecimalField(max_digits=12, decimal_places=3)
    waste_factor_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        ordering = ["recipe", "ingredient"]
        unique_together = [["recipe", "ingredient"]]

    def __str__(self):
        return f"{self.recipe} — {self.ingredient}"


class ProductionBatch(models.Model):
    STATUS_PLANNED = "planned"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PLANNED, "Planned"),
        (STATUS_IN_PROGRESS, "In progress"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="production_batches",
    )
    batch_code = models.CharField(max_length=80)
    production_date = models.DateField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_PLANNED)
    planned_by = models.ForeignKey(
        StaffMember,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="planned_batches",
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-production_date", "batch_code"]
        unique_together = [["workspace", "batch_code"]]

    def __str__(self):
        return self.batch_code


class ProductionBatchLine(models.Model):
    batch = models.ForeignKey(
        ProductionBatch,
        on_delete=models.CASCADE,
        related_name="lines",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.PROTECT,
        related_name="production_lines",
    )
    planned_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    produced_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    failed_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        ordering = ["batch", "recipe"]

    def __str__(self):
        return f"{self.batch} — {self.recipe}"


class BatchAllocation(models.Model):
    batch_line = models.ForeignKey(
        ProductionBatchLine,
        on_delete=models.CASCADE,
        related_name="allocations",
    )
    order_item = models.ForeignKey(
        BakeryOrderItem,
        on_delete=models.CASCADE,
        related_name="batch_allocations",
    )
    allocated_quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["batch_line", "order_item"]
        unique_together = [["batch_line", "order_item"]]

    def __str__(self):
        return f"{self.batch_line} → {self.order_item}"


class WasteRecord(models.Model):
    REASON_EXPIRY = "expiry"
    REASON_OVERPRODUCTION = "overproduction"
    REASON_DAMAGE = "damage"
    REASON_CANCELLATION = "cancellation"
    REASON_RECIPE_ERROR = "recipe_error"
    REASON_QUALITY_ISSUE = "quality_issue"
    REASON_OTHER = "other"

    REASON_CHOICES = [
        (REASON_EXPIRY, "Expiry"),
        (REASON_OVERPRODUCTION, "Overproduction"),
        (REASON_DAMAGE, "Damage"),
        (REASON_CANCELLATION, "Cancellation"),
        (REASON_RECIPE_ERROR, "Recipe error"),
        (REASON_QUALITY_ISSUE, "Quality issue"),
        (REASON_OTHER, "Other"),
    ]

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="waste_records",
    )
    waste_date = models.DateField()
    reason = models.CharField(max_length=40, choices=REASON_CHOICES)
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="waste_records",
    )
    cake = models.ForeignKey(
        "cakes.Cake",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bakeops_waste_records",
    )
    variant = models.ForeignKey(
        "cakes.CakeVariant",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bakeops_waste_records",
    )
    batch_line = models.ForeignKey(
        ProductionBatchLine,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="waste_records",
    )
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-waste_date", "reason"]

    def __str__(self):
        return f"{self.waste_date} — {self.reason} — £{self.estimated_cost}"