from decimal import Decimal

from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL


class CakeCollection(models.Model):
    """
    Front-end collections like:
    - 🎂 Birthday Zone   (key='birthday')
    - 🧸 Kids Collection (key='kids')
    - 🍫 Chocolate Collection (key='chocolate')

    "All Cakes" is a UI filter only, so it is NOT stored here.
    """

    key = models.SlugField(
        max_length=30,
        unique=True,
        help_text="Internal key, e.g. birthday, kids, chocolate.",
    )
    label = models.CharField(
        max_length=100,
        help_text="Display name, e.g. 'Birthday Zone'.",
    )
    icon = models.CharField(
        max_length=10,
        blank=True,
        help_text="Optional emoji icon, e.g. 🎂",
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "label"]

    def __str__(self):
        return self.label


class Cake(models.Model):
    class OccasionType(models.TextChoices):
        WEDDING = "wedding", "💍 Wedding"
        ANNIVERSARY = "anniversary", "💞 Anniversary"
        PARTY = "party", "🎉 Party"
        OTHER = "other", "☕ Everyday / Other"

    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)

    occasion_type = models.CharField(
        max_length=20,
        choices=OccasionType.choices,
        default=OccasionType.OTHER,
    )

    # Free text category, e.g. "Chocolate", "Kids", "Vintage"
    category = models.CharField(
        max_length=100,
        blank=True,
        help_text="Display category, e.g. Chocolate, Kids, Vintage, Photo Cake.",
    )

    short_description = models.CharField(max_length=255)
    description = models.TextField()

    main_image = models.ImageField(
        upload_to="cakes/",
        help_text="Main cake image used on listing and detail pages.",
    )

    # Extra tab fields for the detail page
    code = models.CharField(
        max_length=30,
        blank=True,
        help_text="Optional cake code / SKU shown on detail page.",
    )
    ingredients = models.TextField(
        blank=True,
        help_text="Ingredients list for the Ingredients & Allergy tab.",
    )
    allergy_advice = models.TextField(
        blank=True,
        help_text="Allergy & cross-contamination information.",
    )
    nutrition_info = models.TextField(
        blank=True,
        help_text="Nutritional information (per slice / per 100g).",
    )

    collections = models.ManyToManyField(
        CakeCollection,
        related_name="cakes",
        blank=True,
        help_text="Collections like Birthday Zone, Kids Collection, Chocolate Collection.",
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def default_variant(self):
        """
        Preferred variant shown first on detail page
        (if no is_default is set, fall back to cheapest).
        """
        variant = self.variants.filter(is_default=True).first()
        if variant:
            return variant
        return self.variants.order_by("price").first()


class CakeVariant(models.Model):
    cake = models.ForeignKey(
        Cake,
        related_name="variants",
        on_delete=models.CASCADE,
    )
    # e.g. 6" • serves 6–8
    label = models.CharField(
        max_length=50,
        help_text='Displayed size label, e.g. 6" • serves 6–8',
    )
    serves_min = models.PositiveIntegerField(null=True, blank=True)
    serves_max = models.PositiveIntegerField(null=True, blank=True)

    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_default = models.BooleanField(
        default=False,
        help_text="Use this as the default size/price on the detail page.",
    )

    class Meta:
        ordering = ["price"]

    def __str__(self):
        return f"{self.cake.name} – {self.label}"




class LoyaltyAccount(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="loyalty_account",
    )
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Loyalty account for {self.user} – {self.points} pts"

    @property
    def balance_value(self) -> Decimal:
        """
        Monetary value of points.
        Example rule: 1 point = £0.10
        """
        return Decimal(self.points) * Decimal("0.10")


class Order(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING = "pending", "Pending payment"
        PAID = "paid", "Paid"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Loyalty integration
    points_earned = models.PositiveIntegerField(default=0)
    points_redeemed = models.PositiveIntegerField(default=0)
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Money discount from redeemed points.",
    )

    def __str__(self):
        return f"Order #{self.pk} – {self.status}"

    def calculate_total(self):
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total - self.discount_amount
        return self.total_amount

    def calculate_points_earned(self) -> int:
        """
        Example rule:
        - 1 point for every £5 spent (after discount).
        """
        if self.total_amount <= 0:
            return 0
        return int(self.total_amount // Decimal("5.00"))

    def mark_as_paid(self):
        """
        Call this when payment is confirmed.
        It calculates points and updates the customer's loyalty account.
        """
        self.status = self.Status.PAID
        self.points_earned = self.calculate_points_earned()
        self.save()

        if self.user and self.points_earned > 0:
            account, _ = LoyaltyAccount.objects.get_or_create(user=self.user)
            account.points += self.points_earned
            account.save()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    cake = models.ForeignKey(
        Cake,
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    variant = models.ForeignKey(
        CakeVariant,
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.cake.name} ({self.variant.label}) x {self.quantity}"
class Review(models.Model):
    RATING_CHOICES = [
        (1, "1 – Very poor"),
        (2, "2 – Poor"),
        (3, "3 – Okay"),
        (4, "4 – Good"),
        (5, "5 – Excellent"),
    ]

    cake = models.ForeignKey(
        Cake,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        help_text="1 = poor, 5 = amazing",
    )
    title = models.CharField(max_length=120, blank=True)
    comment = models.TextField()

    # For now, make default True so you actually see them while testing
    is_approved = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this review from the website.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.cake.name} – {self.name} ({self.rating}/5)"
