from django.db import models

from .workspace import Workspace


class Customer(models.Model):
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="customers",
    )
    full_name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_repeat_customer = models.BooleanField(default=False)

    class Meta:
        ordering = ["full_name"]
        unique_together = [["workspace", "email"]]

    def __str__(self):
        return self.full_name


class LoyaltyAccount(models.Model):
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="loyalty_accounts",
    )
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        related_name="bakeops_loyalty_account",
    )
    points_balance = models.PositiveIntegerField(default=0)
    lifetime_points_earned = models.PositiveIntegerField(default=0)
    lifetime_points_redeemed = models.PositiveIntegerField(default=0)
    joined_on = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["customer__full_name"]

    def __str__(self):
        return f"{self.customer} — {self.points_balance} points"


class OccasionType(models.Model):
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="occasion_types",
    )
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        unique_together = [["workspace", "name"]]

    def __str__(self):
        return self.name


class CakeReview(models.Model):
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="cake_reviews",
    )
    cake = models.ForeignKey(
        "cakes.Cake",
        on_delete=models.CASCADE,
        related_name="bakeops_reviews",
    )
    variant = models.ForeignKey(
        "cakes.CakeVariant",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bakeops_reviews",
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cake_reviews",
    )
    rating = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=120, blank=True)
    comment = models.TextField(blank=True)
    review_date = models.DateField()
    is_verified_purchase = models.BooleanField(default=False)

    class Meta:
        ordering = ["-review_date", "cake"]

    def __str__(self):
        return f"{self.cake} — {self.rating}/5"