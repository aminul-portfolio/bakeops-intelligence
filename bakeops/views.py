from decimal import Decimal

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

def product_profitability(request):
    latest_metric = (
        DailyBakeryMetric.objects.select_related("workspace")
        .order_by("-metric_date")
        .first()
    )

    workspace = latest_metric.workspace if latest_metric else None
    snapshot_date = latest_metric.metric_date if latest_metric else None

    product_snapshots = []
    product_rows = []
    signature_product = None

    if workspace and snapshot_date:
        product_snapshots = list(
            ProductPerformanceSnapshot.objects.filter(
                workspace=workspace,
                snapshot_date=snapshot_date,
            )
            .select_related("cake", "variant")
            .order_by("revenue_rank", "cake__name")
        )

        signature_product = _find_signature_product(product_snapshots)
        product_rows = _build_product_profitability_rows(
            product_snapshots=product_snapshots,
            signature_product=signature_product,
        )

    review_count = sum(
        1
        for product in product_snapshots
        if product.action_flag == ProductPerformanceSnapshot.ACTION_REVIEW
    )

    promote_count = sum(
        1
        for product in product_snapshots
        if product.action_flag == ProductPerformanceSnapshot.ACTION_PROMOTE
    )

    inversion_count = sum(
        1
        for row in product_rows
        if row["has_margin_rank_inversion"]
    )

    context = {
        "latest_metric": latest_metric,
        "workspace": workspace,
        "snapshot_date": snapshot_date,
        "product_rows": product_rows,
        "product_count": len(product_snapshots),
        "review_count": review_count,
        "promote_count": promote_count,
        "inversion_count": inversion_count,
        "signature_product": signature_product,
        "flag_legend": _get_product_flag_legend(),
    }

    return render(request, "bakeops/product_profitability.html", context)


def _build_product_profitability_rows(product_snapshots, signature_product=None):
    quantity_ranks = _rank_products(
        product_snapshots,
        key_func=lambda product: (
            product.quantity_sold or 0,
            product.revenue or 0,
        ),
    )

    gross_margin_ranks = _rank_products(
        product_snapshots,
        key_func=lambda product: (
            product.gross_margin_percent or 0,
            product.gross_margin or 0,
        ),
    )

    flag_legend_by_flag = {
        item["flag"]: item
        for item in _get_product_flag_legend()
    }

    rows = []

    for product in product_snapshots:
        revenue_rank = product.revenue_rank or 0
        margin_rank = product.waste_adjusted_margin_rank or 0
        margin_rank_gap = margin_rank - revenue_rank

        flag_detail = flag_legend_by_flag.get(
            product.action_flag,
            flag_legend_by_flag[ProductPerformanceSnapshot.ACTION_STABLE],
        )

        rows.append(
            {
                "product": product,
                "revenue_rank": revenue_rank,
                "quantity_rank": quantity_ranks.get(product.pk),
                "gross_margin_rank": gross_margin_ranks.get(product.pk),
                "waste_adjusted_margin_rank": margin_rank,
                "margin_rank_gap": margin_rank_gap,
                "has_margin_rank_inversion": margin_rank_gap > 0,
                "flag_label": flag_detail["label"],
                "flag_explanation": flag_detail["explanation"],
                "recommended_review": flag_detail["recommended_review"],
                "is_signature": (
                    bool(signature_product)
                    and product.pk == signature_product.pk
                ),
            }
        )

    return rows


def _rank_products(product_snapshots, key_func):
    ranked_products = sorted(
        product_snapshots,
        key=key_func,
        reverse=True,
    )

    return {
        product.pk: index + 1
        for index, product in enumerate(ranked_products)
    }


def _get_product_flag_legend():
    return [
        {
            "flag": ProductPerformanceSnapshot.ACTION_PROMOTE,
            "label": "Promote",
            "explanation": (
                "The product has stronger waste-adjusted margin performance "
                "than its revenue rank suggests."
            ),
            "recommended_review": (
                "Consider giving this product more visibility, offers, or "
                "production priority if demand remains healthy."
            ),
        },
        {
            "flag": ProductPerformanceSnapshot.ACTION_STABLE,
            "label": "Stable",
            "explanation": (
                "The product has broadly aligned revenue and margin performance."
            ),
            "recommended_review": (
                "Keep monitoring after each metric build. No urgent action is "
                "required from this signal alone."
            ),
        },
        {
            "flag": ProductPerformanceSnapshot.ACTION_REVIEW,
            "label": "Review",
            "explanation": (
                "The product sells strongly, but its waste-adjusted margin rank "
                "is weaker than its revenue rank."
            ),
            "recommended_review": (
                "Review recipe cost, waste causes, pricing, batch size, and "
                "production planning before promoting further."
            ),
        },
        {
            "flag": ProductPerformanceSnapshot.ACTION_REDUCE,
            "label": "Reduce",
            "explanation": (
                "The product has weak waste-adjusted margin performance."
            ),
            "recommended_review": (
                "Reduce production pressure or investigate cost and waste issues "
                "before pushing additional sales."
            ),
        },
    ]

def ingredient_risk(request):
    latest_metric = (
        DailyBakeryMetric.objects.select_related("workspace")
        .order_by("-metric_date")
        .first()
    )

    workspace = latest_metric.workspace if latest_metric else None
    snapshot_date = latest_metric.metric_date if latest_metric else None

    ingredient_snapshots = []
    ingredient_rows = []
    risk_rows = []
    top_risk_ingredient = None
    total_ingredient_cost = Decimal("0.00")
    total_waste_cost = Decimal("0.00")
    near_expiry_lot_count = 0

    if workspace and snapshot_date:
        ingredient_snapshots = list(
            IngredientUsageSnapshot.objects.filter(
                workspace=workspace,
                snapshot_date=snapshot_date,
            )
            .select_related("ingredient", "ingredient__supplier")
            .order_by("ingredient__name")
        )

        ingredient_rows = _build_ingredient_risk_rows(ingredient_snapshots)
        risk_rows = [
            row
            for row in ingredient_rows
            if row["snapshot"].stock_risk_level != IngredientUsageSnapshot.RISK_LOW
        ]

        top_risk_ingredient = risk_rows[0] if risk_rows else None

        total_ingredient_cost = sum(
            (snapshot.ingredient_cost for snapshot in ingredient_snapshots),
            Decimal("0.00"),
        )

        total_waste_cost = sum(
            (snapshot.waste_cost for snapshot in ingredient_snapshots),
            Decimal("0.00"),
        )

        near_expiry_lot_count = sum(
            snapshot.near_expiry_lot_count
            for snapshot in ingredient_snapshots
        )

    context = {
        "latest_metric": latest_metric,
        "workspace": workspace,
        "snapshot_date": snapshot_date,
        "ingredient_rows": ingredient_rows,
        "risk_rows": risk_rows,
        "top_risk_ingredient": top_risk_ingredient,
        "ingredient_count": len(ingredient_snapshots),
        "risk_count": len(risk_rows),
        "total_ingredient_cost": total_ingredient_cost,
        "total_waste_cost": total_waste_cost,
        "near_expiry_lot_count": near_expiry_lot_count,
        "risk_legend": _get_ingredient_risk_legend(),
    }

    return render(request, "bakeops/ingredient_risk.html", context)


def _build_ingredient_risk_rows(ingredient_snapshots):
    risk_priority = {
        IngredientUsageSnapshot.RISK_CRITICAL: 1,
        IngredientUsageSnapshot.RISK_HIGH: 2,
        IngredientUsageSnapshot.RISK_MEDIUM: 3,
        IngredientUsageSnapshot.RISK_LOW: 4,
    }

    rows = []

    for snapshot in ingredient_snapshots:
        current_stock = snapshot.current_stock_quantity or Decimal("0.000")
        reorder_level = snapshot.reorder_level_quantity or Decimal("0.000")
        stock_gap = current_stock - reorder_level

        shortage_quantity = Decimal("0.000")
        if current_stock < reorder_level:
            shortage_quantity = reorder_level - current_stock

        waste_rate_percent = _calculate_ingredient_waste_rate(snapshot)

        rows.append(
            {
                "snapshot": snapshot,
                "ingredient": snapshot.ingredient,
                "risk_priority": risk_priority.get(
                    snapshot.stock_risk_level,
                    risk_priority[IngredientUsageSnapshot.RISK_LOW],
                ),
                "risk_label": snapshot.get_stock_risk_level_display(),
                "risk_explanation": _get_ingredient_risk_explanation(snapshot),
                "recommended_action": _get_ingredient_recommended_action(snapshot),
                "current_stock": current_stock,
                "reorder_level": reorder_level,
                "stock_gap": stock_gap,
                "shortage_quantity": shortage_quantity,
                "waste_rate_percent": waste_rate_percent,
                "is_stock_below_reorder": current_stock < reorder_level,
                "has_near_expiry_risk": snapshot.near_expiry_lot_count > 0,
            }
        )

    return sorted(
        rows,
        key=lambda row: (
            row["risk_priority"],
            -row["shortage_quantity"],
            row["ingredient"].name,
        ),
    )


def _calculate_ingredient_waste_rate(snapshot):
    quantity_used = snapshot.quantity_used or Decimal("0.000")
    quantity_wasted = snapshot.quantity_wasted or Decimal("0.000")

    if quantity_used <= 0 and quantity_wasted > 0:
        return Decimal("100.00")

    if quantity_used <= 0:
        return Decimal("0.00")

    return (
        (quantity_wasted / quantity_used) * Decimal("100")
    ).quantize(Decimal("0.01"))


def _get_ingredient_risk_explanation(snapshot):
    if snapshot.stock_risk_level == IngredientUsageSnapshot.RISK_CRITICAL:
        return (
            "This ingredient is at critical stock risk and may block upcoming "
            "production if not reviewed immediately."
        )

    if snapshot.stock_risk_level == IngredientUsageSnapshot.RISK_HIGH:
        return (
            "Current stock is below the reorder level, so this ingredient needs "
            "reorder or supplier review before production pressure increases."
        )

    if snapshot.stock_risk_level == IngredientUsageSnapshot.RISK_MEDIUM:
        return (
            "This ingredient is approaching operational risk and should be "
            "monitored before the next production cycle."
        )

    return (
        "Current stock is above the reorder level. No urgent stock action is "
        "required from this signal alone."
    )


def _get_ingredient_recommended_action(snapshot):
    if snapshot.stock_risk_level in {
        IngredientUsageSnapshot.RISK_CRITICAL,
        IngredientUsageSnapshot.RISK_HIGH,
    }:
        return (
            "Check supplier lead time, reorder quantity, upcoming batch demand, "
            "and any avoidable waste before the next production run."
        )

    if snapshot.near_expiry_lot_count > 0:
        return (
            "Review near-expiry lots and prioritise usage before expiry-driven "
            "waste increases."
        )

    if snapshot.quantity_wasted > 0:
        return (
            "Review waste records and batch allocation to understand whether "
            "waste is avoidable."
        )

    return (
        "Continue monitoring after the next metric build. No immediate action "
        "is required."
    )


def _get_ingredient_risk_legend():
    return [
        {
            "level": "Critical",
            "code": IngredientUsageSnapshot.RISK_CRITICAL,
            "meaning": "Immediate production or stock continuity risk.",
        },
        {
            "level": "High",
            "code": IngredientUsageSnapshot.RISK_HIGH,
            "meaning": "Current stock is below reorder level and needs review.",
        },
        {
            "level": "Medium",
            "code": IngredientUsageSnapshot.RISK_MEDIUM,
            "meaning": "Approaching risk threshold; monitor before next production cycle.",
        },
        {
            "level": "Low",
            "code": IngredientUsageSnapshot.RISK_LOW,
            "meaning": "Stock is currently above reorder level.",
        },
    ]

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