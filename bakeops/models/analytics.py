from decimal import Decimal

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from .catalog import Customer, OccasionType
from .ingredients import Ingredient
from .workspace import Workspace


class DailyBakeryMetric(models.Model):
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="daily_bakery_metrics",
    )
    metric_date = models.DateField()

    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    paid_orders = models.PositiveIntegerField(default=0)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    total_items_sold = models.PositiveIntegerField(default=0)

    ingredient_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    gross_margin = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    gross_margin_percent = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal("0.00"))

    waste_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    waste_adjusted_margin = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    waste_adjusted_margin_percent = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-metric_date"]
        unique_together = [["workspace", "metric_date"]]
        verbose_name = "Daily bakery metric"
        verbose_name_plural = "Daily bakery metrics"

    def __str__(self):
        return f"{self.workspace} — {self.metric_date}"


class ProductPerformanceSnapshot(models.Model):
    ACTION_PROMOTE = "promote"
    ACTION_STABLE = "stable"
    ACTION_REVIEW = "review"
    ACTION_REDUCE = "reduce"

    ACTION_CHOICES = [
        (ACTION_PROMOTE, "Promote"),
        (ACTION_STABLE, "Stable"),
        (ACTION_REVIEW, "Review"),
        (ACTION_REDUCE, "Reduce"),
    ]

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="product_performance_snapshots",
    )
    snapshot_date = models.DateField()

    cake = models.ForeignKey(
        "cakes.Cake",
        on_delete=models.CASCADE,
        related_name="bakeops_performance_snapshots",
    )
    variant = models.ForeignKey(
        "cakes.CakeVariant",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bakeops_performance_snapshots",
    )

    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    quantity_sold = models.PositiveIntegerField(default=0)
    paid_order_count = models.PositiveIntegerField(default=0)

    ingredient_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    gross_margin = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    gross_margin_percent = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal("0.00"))

    waste_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    waste_adjusted_margin = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    waste_adjusted_margin_percent = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    revenue_rank = models.PositiveIntegerField(null=True, blank=True)
    waste_adjusted_margin_rank = models.PositiveIntegerField(null=True, blank=True)

    action_flag = models.CharField(
        max_length=30,
        choices=ACTION_CHOICES,
        default=ACTION_STABLE,
    )
    action_reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["snapshot_date", "revenue_rank", "cake"]
        verbose_name = "Product performance snapshot"
        verbose_name_plural = "Product performance snapshots"

    def __str__(self):
        return f"{self.snapshot_date} — {self.cake}"


class IngredientUsageSnapshot(models.Model):
    RISK_LOW = "low"
    RISK_MEDIUM = "medium"
    RISK_HIGH = "high"
    RISK_CRITICAL = "critical"

    RISK_CHOICES = [
        (RISK_LOW, "Low"),
        (RISK_MEDIUM, "Medium"),
        (RISK_HIGH, "High"),
        (RISK_CRITICAL, "Critical"),
    ]

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="ingredient_usage_snapshots",
    )
    snapshot_date = models.DateField()

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="usage_snapshots",
    )

    quantity_used = models.DecimalField(max_digits=12, decimal_places=3, default=Decimal("0.000"))
    quantity_wasted = models.DecimalField(max_digits=12, decimal_places=3, default=Decimal("0.000"))

    ingredient_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    waste_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    current_stock_quantity = models.DecimalField(max_digits=12, decimal_places=3, default=Decimal("0.000"))
    reorder_level_quantity = models.DecimalField(max_digits=12, decimal_places=3, default=Decimal("0.000"))

    stock_risk_level = models.CharField(max_length=30, choices=RISK_CHOICES, default=RISK_LOW)
    near_expiry_lot_count = models.PositiveIntegerField(default=0)
    nearest_expiry_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["snapshot_date", "stock_risk_level", "ingredient"]
        unique_together = [["workspace", "snapshot_date", "ingredient"]]
        verbose_name = "Ingredient usage snapshot"
        verbose_name_plural = "Ingredient usage snapshots"

    def __str__(self):
        return f"{self.snapshot_date} — {self.ingredient}"


class OccasionDemandSnapshot(models.Model):
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="occasion_demand_snapshots",
    )
    snapshot_date = models.DateField()

    occasion = models.ForeignKey(
        OccasionType,
        on_delete=models.CASCADE,
        related_name="demand_snapshots",
    )

    order_count = models.PositiveIntegerField(default=0)
    quantity_sold = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    gross_margin = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    upcoming_order_count = models.PositiveIntegerField(default=0)
    delivery_slot_pressure_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["snapshot_date", "occasion"]
        unique_together = [["workspace", "snapshot_date", "occasion"]]
        verbose_name = "Occasion demand snapshot"
        verbose_name_plural = "Occasion demand snapshots"

    def __str__(self):
        return f"{self.snapshot_date} — {self.occasion}"


class CustomerLoyaltySnapshot(models.Model):
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="customer_loyalty_snapshots",
    )
    snapshot_date = models.DateField()

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="loyalty_snapshots",
    )

    total_orders = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))

    loyalty_points_earned = models.PositiveIntegerField(default=0)
    loyalty_points_redeemed = models.PositiveIntegerField(default=0)
    current_points_balance = models.PositiveIntegerField(default=0)

    is_repeat_customer = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["snapshot_date", "customer"]
        unique_together = [["workspace", "snapshot_date", "customer"]]
        verbose_name = "Customer loyalty snapshot"
        verbose_name_plural = "Customer loyalty snapshots"

    def __str__(self):
        return f"{self.snapshot_date} — {self.customer}"


class BakeryMetricRunLog(models.Model):
    STATUS_STARTED = "started"
    STATUS_SUCCESS = "success"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_STARTED, "Started"),
        (STATUS_SUCCESS, "Success"),
        (STATUS_FAILED, "Failed"),
    ]

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="metric_run_logs",
    )
    command_name = models.CharField(max_length=120, default="build_bakery_metrics")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_STARTED)

    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)

    rows_processed = models.PositiveIntegerField(default=0)
    metrics_created = models.PositiveIntegerField(default=0)
    snapshots_created = models.PositiveIntegerField(default=0)
    issues_created = models.PositiveIntegerField(default=0)

    error_message = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-started_at"]
        verbose_name = "Bakery metric run log"
        verbose_name_plural = "Bakery metric run logs"

    def __str__(self):
        return f"{self.command_name} — {self.status} — {self.started_at:%Y-%m-%d %H:%M}"


class DataQualityIssue(models.Model):
    SEVERITY_INFO = "info"
    SEVERITY_WARNING = "warning"
    SEVERITY_ERROR = "error"
    SEVERITY_CRITICAL = "critical"

    SEVERITY_CHOICES = [
        (SEVERITY_INFO, "Info"),
        (SEVERITY_WARNING, "Warning"),
        (SEVERITY_ERROR, "Error"),
        (SEVERITY_CRITICAL, "Critical"),
    ]

    STATUS_OPEN = "open"
    STATUS_RESOLVED = "resolved"
    STATUS_IGNORED = "ignored"

    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_RESOLVED, "Resolved"),
        (STATUS_IGNORED, "Ignored"),
    ]

    ISSUE_ACTIVE_CAKE_WITHOUT_VARIANT = "active_cake_without_variant"
    ISSUE_VARIANT_WITHOUT_RECIPE = "variant_without_recipe"
    ISSUE_RECIPE_WITHOUT_LINES = "recipe_without_lines"
    ISSUE_PAID_ORDER_WITHOUT_ITEMS = "paid_order_without_items"
    ISSUE_ZERO_TOTAL_ORDER = "zero_total_order"
    ISSUE_LOW_STOCK = "low_stock"
    ISSUE_NEAR_EXPIRY = "near_expiry"
    ISSUE_WASTE_WITHOUT_REASON = "waste_without_reason"
    ISSUE_PRODUCTION_UNDER_DEMAND = "production_under_demand"
    ISSUE_UNALLOCATED_PRODUCTION = "unallocated_production"

    ISSUE_TYPE_CHOICES = [
        (ISSUE_ACTIVE_CAKE_WITHOUT_VARIANT, "Active cake without variant"),
        (ISSUE_VARIANT_WITHOUT_RECIPE, "Cake variant without recipe"),
        (ISSUE_RECIPE_WITHOUT_LINES, "Recipe without recipe lines"),
        (ISSUE_PAID_ORDER_WITHOUT_ITEMS, "Paid order without order items"),
        (ISSUE_ZERO_TOTAL_ORDER, "Order with zero total"),
        (ISSUE_LOW_STOCK, "Ingredient below reorder level"),
        (ISSUE_NEAR_EXPIRY, "Ingredient lot close to expiry"),
        (ISSUE_WASTE_WITHOUT_REASON, "Waste record without reason"),
        (ISSUE_PRODUCTION_UNDER_DEMAND, "Production batch under-produced vs demand"),
        (ISSUE_UNALLOCATED_PRODUCTION, "Production output not allocated to orders"),
    ]

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="data_quality_issues",
    )

    issue_type = models.CharField(max_length=80, choices=ISSUE_TYPE_CHOICES)
    severity = models.CharField(max_length=30, choices=SEVERITY_CHOICES, default=SEVERITY_WARNING)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_OPEN)

    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    suggested_action = models.TextField(blank=True)

    affected_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    affected_object_id = models.PositiveIntegerField(null=True, blank=True)
    affected_object = GenericForeignKey("affected_content_type", "affected_object_id")

    detected_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["status", "-severity", "-detected_at"]
        verbose_name = "Data quality issue"
        verbose_name_plural = "Data quality issues"

    def __str__(self):
        return f"{self.get_severity_display()} — {self.title}"