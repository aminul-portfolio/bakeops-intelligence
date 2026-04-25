from decimal import Decimal

from django.db import models

from .catalog import Customer, OccasionType
from .workspace import Workspace


class DeliverySlot(models.Model):
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="delivery_slots",
    )
    slot_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity_orders = models.PositiveIntegerField(default=10)
    booked_orders = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["slot_date", "start_time"]

    def __str__(self):
        return f"{self.slot_date} {self.start_time}-{self.end_time}"


class BakeryOrder(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_CONFIRMED = "confirmed"
    STATUS_PAID = "paid"
    STATUS_FULFILLED = "fulfilled"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_PAID, "Paid"),
        (STATUS_FULFILLED, "Fulfilled"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    CHANNEL_WEBSITE = "website"
    CHANNEL_PHONE = "phone"
    CHANNEL_IN_STORE = "in_store"
    CHANNEL_SOCIAL = "social"

    CHANNEL_CHOICES = [
        (CHANNEL_WEBSITE, "Website"),
        (CHANNEL_PHONE, "Phone"),
        (CHANNEL_IN_STORE, "In store"),
        (CHANNEL_SOCIAL, "Social"),
    ]

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="bakery_orders",
    )
    order_number = models.CharField(max_length=40)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bakery_orders",
    )
    occasion = models.ForeignKey(
        OccasionType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bakery_orders",
    )
    delivery_slot = models.ForeignKey(
        DeliverySlot,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bakery_orders",
    )
    order_date = models.DateField()
    required_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    channel = models.CharField(max_length=30, choices=CHANNEL_CHOICES, default=CHANNEL_WEBSITE)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    loyalty_points_earned = models.PositiveIntegerField(default=0)
    loyalty_points_redeemed = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-order_date", "order_number"]
        unique_together = [["workspace", "order_number"]]

    def __str__(self):
        return f"{self.order_number} — {self.total_amount}"


class BakeryOrderItem(models.Model):
    order = models.ForeignKey(
        BakeryOrder,
        on_delete=models.CASCADE,
        related_name="items",
    )
    cake = models.ForeignKey(
        "cakes.Cake",
        on_delete=models.PROTECT,
        related_name="bakeops_order_items",
    )
    variant = models.ForeignKey(
        "cakes.CakeVariant",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bakeops_order_items",
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)
    special_instructions = models.TextField(blank=True)

    class Meta:
        ordering = ["order", "cake"]

    def __str__(self):
        return f"{self.order.order_number} — {self.cake} x {self.quantity}"