from decimal import Decimal
from types import SimpleNamespace

from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ReviewForm
from .models import Cake, CakeCollection


def _money(value):
    """
    Format a numeric value as a GBP currency string for the temporary V1 dashboard.

    This keeps the current templates usable before the real BakeOps gold-layer
    reporting models are implemented.
    """
    try:
        return f"£{Decimal(value):,.0f}"
    except Exception:
        return "£0"


def _variant_price(variant, fallback=Decimal("25.00")):
    """
    Safely read a variant price from the existing cake catalogue model.
    """
    if not variant:
        return fallback

    price = getattr(variant, "price", None)
    if price is None:
        return fallback

    try:
        return Decimal(price)
    except Exception:
        return fallback


def _build_placeholder_product_snapshots(cakes):
    """
    Temporary V1 bridge.

    These rows allow the revised BakeOps Intelligence dashboard to render from the
    existing cake catalogue while the real V1 models are being built:

    - ProductPerformanceSnapshot
    - DailyBakeryMetric
    - IngredientUsageSnapshot
    - DataQualityIssue
    - BakeryMetricRunLog

    Replace this helper once build_bakery_metrics creates real reporting rows.
    """
    margin_profiles = [
        {
            "quantity": Decimal("86"),
            "gross_margin_percent": Decimal("31"),
            "waste_adjusted_margin_percent": Decimal("18"),
            "note": "Best-seller with waste pressure",
        },
        {
            "quantity": Decimal("42"),
            "gross_margin_percent": Decimal("52"),
            "waste_adjusted_margin_percent": Decimal("49"),
            "note": "High margin, rising demand",
        },
        {
            "quantity": Decimal("31"),
            "gross_margin_percent": Decimal("44"),
            "waste_adjusted_margin_percent": Decimal("41"),
            "note": "Stable premium order profile",
        },
        {
            "quantity": Decimal("24"),
            "gross_margin_percent": Decimal("14"),
            "waste_adjusted_margin_percent": Decimal("7"),
            "note": "Low demand and weak adjusted margin",
        },
    ]

    snapshots = []

    for index, cake in enumerate(cakes[:4]):
        variant = None

        try:
            variant = cake.default_variant()
        except Exception:
            try:
                variant = cake.variants.all().order_by("price").first()
            except Exception:
                variant = None

        profile = margin_profiles[index % len(margin_profiles)]
        price = _variant_price(variant)
        revenue = price * profile["quantity"]

        snapshots.append(
            SimpleNamespace(
                cake=cake,
                variant=variant or SimpleNamespace(name="Standard variant"),
                revenue=_money(revenue),
                gross_margin_percent=profile["gross_margin_percent"],
                waste_adjusted_margin_percent=profile["waste_adjusted_margin_percent"],
                note=profile["note"],
            )
        )

    return snapshots


def home(request):
    """
    BakeOps Intelligence V1 landing surface.

    Current role:
    - Render the revised analytics-first homepage.
    - Use the existing Cake catalogue as temporary demo input.
    - Provide safe placeholder metrics until the real BakeOps V1 reporting
      models and build_bakery_metrics command are implemented.

    Future role:
    - Replace placeholder values with DailyBakeryMetric, ProductPerformanceSnapshot,
      IngredientUsageSnapshot, DataQualityIssue, and weekly recommendation records.
    """
    cakes = list(
        Cake.objects
        .filter(is_active=True)
        .prefetch_related("variants", "collections")
        .order_by("name")[:8]
    )

    product_snapshots = _build_placeholder_product_snapshots(cakes)

    context = {
        "total_revenue": "£18,240",
        "paid_orders": 147,
        "average_order_value": "£124",
        "gross_margin_percent": "38.4%",
        "total_waste_cost": "£892",
        "product_snapshots": product_snapshots,
        "data_quality_issues": [
            SimpleNamespace(
                severity="Critical",
                issue_type="Missing recipe",
                message="A product without recipe lines cannot produce trusted ingredient cost or margin.",
            ),
            SimpleNamespace(
                severity="Medium",
                issue_type="Low stock ingredient",
                message="Unsalted butter is below reorder level before upcoming production demand.",
            ),
            SimpleNamespace(
                severity="Medium",
                issue_type="Near-expiry lot",
                message="Double cream should be used in planned production before expiry risk increases.",
            ),
        ],
        "weekly_actions": [
            SimpleNamespace(
                priority="Promote",
                title="Promote high-margin product",
                reason="Seasonal Fruit Gateau has stronger waste-adjusted margin and enough stock coverage.",
            ),
            SimpleNamespace(
                priority="Review",
                title="Review best-seller margin",
                reason="Birthday Classic performs well by revenue but weakens after waste cost is included.",
            ),
            SimpleNamespace(
                priority="Reorder",
                title="Reorder key ingredient",
                reason="Unsalted butter is below reorder level before upcoming production demand.",
            ),
        ],
    }

    return render(request, "cakes/home.html", context)


def cake_list(request):
    """
    Product profitability reference page.

    This keeps your existing cake catalogue available, but positions it as
    the source catalogue that will feed BakeOps V1 seed data, recipe costing,
    reviews, and ProductPerformanceSnapshot records.
    """
    cakes = (
        Cake.objects
        .filter(is_active=True)
        .prefetch_related("variants", "collections")
        .order_by("name")
    )

    collections = (
        CakeCollection.objects
        .filter(is_active=True)
        .order_by("sort_order")
    )

    return render(
        request,
        "cakes/cakes.html",
        {
            "cakes": cakes,
            "collections": collections,
        },
    )


def cake_detail(request, slug):
    """
    Existing single-cake detail page.

    Keep this for now because it is useful catalogue/reference functionality.
    It can later become a product inspection page or be replaced by a proper
    BakeOps product profitability detail surface.
    """
    cake = get_object_or_404(Cake, slug=slug, is_active=True)

    variants = cake.variants.all().order_by("price")
    default_variant = cake.default_variant()

    reviews = cake.reviews.filter(is_approved=True)
    review_count = reviews.count()
    average_rating = (
        reviews.aggregate(avg=Avg("rating"))["avg"] if review_count else None
    )

    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.cake = cake
            review.save()
            return redirect("cake_detail", slug=cake.slug)
    else:
        review_form = ReviewForm()

    related_cakes = (
        Cake.objects.filter(is_active=True, occasion_type=cake.occasion_type)
        .exclude(id=cake.id)
        .order_by("name")[:4]
    )

    return render(
        request,
        "cakes/cake_detail.html",
        {
            "cake": cake,
            "variants": variants,
            "default_variant": default_variant,
            "reviews": reviews,
            "review_count": review_count,
            "average_rating": average_rating,
            "review_form": review_form,
            "related_cakes": related_cakes,
        },
    )


def offers(request):
    """
    Legacy route kept temporarily so existing URLs do not break.

    Recommendation:
    Remove this route from the main navigation during BakeOps V1.
    """
    return render(request, "cakes/offers.html")


def about(request):
    """
    Legacy route kept temporarily so existing URLs do not break.

    Recommendation:
    Remove this route from the main navigation during BakeOps V1.
    """
    return render(request, "cakes/about.html")


def contact(request):
    """
    Reframed by the revised template as the BI exports and reviewer walkthrough page.
    """
    return render(request, "cakes/contact.html")


def welcome(request):
    """
    Reframed by the revised template as the data quality and trust layer page.
    """
    return render(request, "cakes/welcome.html")
