from django.shortcuts import render

from .models import (
    BakeryMetricRunLog,
    CustomerLoyaltySnapshot,
    DailyBakeryMetric,
    DataQualityIssue,
    IngredientUsageSnapshot,
    OccasionDemandSnapshot,
    ProductPerformanceSnapshot,
)


def analytics_dashboard(request):
    latest_metric = (
        DailyBakeryMetric.objects.select_related("workspace")
        .order_by("-metric_date")
        .first()
    )

    workspace = latest_metric.workspace if latest_metric else None
    snapshot_date = latest_metric.metric_date if latest_metric else None

    product_snapshots = []
    ingredient_risks = []
    occasion_snapshots = []
    customer_snapshots = []
    data_quality_issues = []
    last_run_log = None
    signature_product = None
    weekly_actions = []

    if workspace and snapshot_date:
        product_snapshots = list(
            ProductPerformanceSnapshot.objects.filter(
                workspace=workspace,
                snapshot_date=snapshot_date,
            )
            .select_related("cake", "variant")
            .order_by("revenue_rank", "cake__name")
        )

        ingredient_risks = list(
            IngredientUsageSnapshot.objects.filter(
                workspace=workspace,
                snapshot_date=snapshot_date,
            )
            .select_related("ingredient")
            .exclude(stock_risk_level=IngredientUsageSnapshot.RISK_LOW)
            .order_by("stock_risk_level", "ingredient__name")[:8]
        )

        occasion_snapshots = list(
            OccasionDemandSnapshot.objects.filter(
                workspace=workspace,
                snapshot_date=snapshot_date,
            )
            .select_related("occasion")
            .order_by("-revenue", "occasion__name")[:6]
        )

        customer_snapshots = list(
            CustomerLoyaltySnapshot.objects.filter(
                workspace=workspace,
                snapshot_date=snapshot_date,
            )
            .select_related("customer")
            .order_by("-total_revenue", "customer__full_name")[:6]
        )

        data_quality_issues = list(
            DataQualityIssue.objects.filter(
                workspace=workspace,
                status=DataQualityIssue.STATUS_OPEN,
            )
            .order_by("-detected_at")[:8]
        )

        last_run_log = (
            BakeryMetricRunLog.objects.filter(workspace=workspace)
            .order_by("-started_at")
            .first()
        )

        signature_product = _find_signature_product(product_snapshots)
        weekly_actions = _build_weekly_actions(
            product_snapshots=product_snapshots,
            ingredient_risks=ingredient_risks,
            data_quality_issues=data_quality_issues,
        )

    context = {
        "latest_metric": latest_metric,
        "workspace": workspace,
        "snapshot_date": snapshot_date,
        "product_snapshots": product_snapshots,
        "ingredient_risks": ingredient_risks,
        "occasion_snapshots": occasion_snapshots,
        "customer_snapshots": customer_snapshots,
        "data_quality_issues": data_quality_issues,
        "last_run_log": last_run_log,
        "signature_product": signature_product,
        "weekly_actions": weekly_actions,
    }

    return render(request, "bakeops/analytics_dashboard.html", context)


def _find_signature_product(product_snapshots):
    for product in product_snapshots:
        if (
            product.revenue_rank == 1
            and product.waste_adjusted_margin_rank
            and product.waste_adjusted_margin_rank > product.revenue_rank
        ):
            return product

    return None


def _build_weekly_actions(product_snapshots, ingredient_risks, data_quality_issues):
    actions = []

    for product in product_snapshots:
        if product.action_flag == ProductPerformanceSnapshot.ACTION_REVIEW:
            actions.append(
                {
                    "priority": "High",
                    "title": f"Review {product.cake.name}",
                    "metric": (
                        f"Revenue rank #{product.revenue_rank}, "
                        f"waste-adjusted margin rank #{product.waste_adjusted_margin_rank}"
                    ),
                    "reason": product.action_reason,
                    "action": "Review recipe cost, waste causes, pricing, and production quantity.",
                }
            )

        if product.action_flag == ProductPerformanceSnapshot.ACTION_PROMOTE:
            actions.append(
                {
                    "priority": "Medium",
                    "title": f"Promote {product.cake.name}",
                    "metric": (
                        f"Waste-adjusted margin rank #{product.waste_adjusted_margin_rank}"
                    ),
                    "reason": product.action_reason,
                    "action": "Feature this product in offers, homepage placement, or weekly recommendations.",
                }
            )

    for ingredient in ingredient_risks[:2]:
        actions.append(
            {
                "priority": "High",
                "title": f"Reorder or review {ingredient.ingredient.name}",
                "metric": f"Stock risk: {ingredient.get_stock_risk_level_display()}",
                "reason": (
                    f"Current stock is {ingredient.current_stock_quantity}; "
                    f"reorder level is {ingredient.reorder_level_quantity}."
                ),
                "action": "Check supplier lead time and reorder before upcoming production demand.",
            }
        )

    for issue in data_quality_issues[:2]:
        actions.append(
            {
                "priority": issue.get_severity_display(),
                "title": issue.title,
                "metric": issue.get_issue_type_display(),
                "reason": issue.description or "Open data quality issue requires review.",
                "action": issue.suggested_action or "Review and resolve this issue in admin.",
            }
        )

    if not actions:
        actions.append(
            {
                "priority": "Info",
                "title": "No urgent weekly action found",
                "metric": "All core signals are currently stable",
                "reason": "The latest metric build did not surface urgent product, ingredient, or data quality actions.",
                "action": "Continue monitoring the dashboard after the next metric build.",
            }
        )

    return actions[:6]