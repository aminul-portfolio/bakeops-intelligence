from decimal import Decimal

from django.db.models import Sum
from django.shortcuts import render

from .models import (
    BakeryMetricRunLog,
    CustomerLoyaltySnapshot,
    DailyBakeryMetric,
    DataQualityIssue,
    IngredientUsageSnapshot,
    OccasionDemandSnapshot,
    ProductPerformanceSnapshot,
    WasteRecord,
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
def waste_analysis(request):
    latest_metric = (
        DailyBakeryMetric.objects.select_related("workspace")
        .order_by("-metric_date")
        .first()
    )

    workspace = latest_metric.workspace if latest_metric else None
    snapshot_date = latest_metric.metric_date if latest_metric else None

    waste_records = []
    product_waste_rows = []
    ingredient_waste_rows = []
    waste_reason_rows = []
    top_waste_product = None

    total_waste_cost = Decimal("0.00")
    total_waste_records = 0
    gross_margin = Decimal("0.00")
    waste_adjusted_margin = Decimal("0.00")
    waste_margin_impact_percent = Decimal("0.00")

    if workspace and snapshot_date:
        waste_records = list(
            WasteRecord.objects.filter(workspace=workspace)
            .select_related("cake", "variant", "ingredient")
            .order_by("-estimated_cost", "reason")
        )

        product_snapshots = list(
            ProductPerformanceSnapshot.objects.filter(
                workspace=workspace,
                snapshot_date=snapshot_date,
            )
            .select_related("cake", "variant")
            .order_by("-waste_cost", "cake__name")
        )

        ingredient_snapshots = list(
            IngredientUsageSnapshot.objects.filter(
                workspace=workspace,
                snapshot_date=snapshot_date,
                waste_cost__gt=0,
            )
            .select_related("ingredient")
            .order_by("-waste_cost", "ingredient__name")
        )

        total_waste_cost = (
            WasteRecord.objects.filter(workspace=workspace)
            .aggregate(total=Sum("estimated_cost"))
            .get("total")
            or Decimal("0.00")
        )

        total_waste_records = len(waste_records)
        gross_margin = latest_metric.gross_margin or Decimal("0.00")
        waste_adjusted_margin = latest_metric.waste_adjusted_margin or Decimal("0.00")
        waste_margin_impact_percent = _calculate_waste_margin_impact_percent(
            total_waste_cost=total_waste_cost,
            gross_margin=gross_margin,
        )

        product_waste_rows = _build_product_waste_rows(product_snapshots)
        ingredient_waste_rows = _build_ingredient_waste_rows(ingredient_snapshots)
        waste_reason_rows = _build_waste_reason_rows(waste_records)

        top_waste_product = product_waste_rows[0] if product_waste_rows else None

    context = {
        "latest_metric": latest_metric,
        "workspace": workspace,
        "snapshot_date": snapshot_date,
        "waste_records": waste_records,
        "total_waste_records": total_waste_records,
        "total_waste_cost": total_waste_cost,
        "gross_margin": gross_margin,
        "waste_adjusted_margin": waste_adjusted_margin,
        "waste_margin_impact_percent": waste_margin_impact_percent,
        "product_waste_rows": product_waste_rows,
        "ingredient_waste_rows": ingredient_waste_rows,
        "waste_reason_rows": waste_reason_rows,
        "top_waste_product": top_waste_product,
    }

    return render(request, "bakeops/waste_analysis.html", context)


def _calculate_waste_margin_impact_percent(total_waste_cost, gross_margin):
    if not gross_margin or gross_margin <= 0:
        return Decimal("0.00")

    return (
        (total_waste_cost / gross_margin) * Decimal("100")
    ).quantize(Decimal("0.01"))


def _build_product_waste_rows(product_snapshots):
    rows = []

    for snapshot in product_snapshots:
        waste_cost = snapshot.waste_cost or Decimal("0.00")
        gross_margin = snapshot.gross_margin or Decimal("0.00")
        waste_adjusted_margin = snapshot.waste_adjusted_margin or Decimal("0.00")

        waste_share_percent = Decimal("0.00")
        if gross_margin > 0:
            waste_share_percent = (
                (waste_cost / gross_margin) * Decimal("100")
            ).quantize(Decimal("0.01"))

        rows.append(
            {
                "snapshot": snapshot,
                "cake": snapshot.cake,
                "variant": snapshot.variant,
                "waste_cost": waste_cost,
                "gross_margin": gross_margin,
                "waste_adjusted_margin": waste_adjusted_margin,
                "waste_share_percent": waste_share_percent,
                "action_flag": snapshot.action_flag,
                "action_label": snapshot.get_action_flag_display(),
                "recommended_action": _get_waste_product_recommended_action(snapshot),
                "is_top_waste_product": False,
            }
        )

    rows = sorted(
        rows,
        key=lambda row: (
            -row["waste_cost"],
            row["cake"].name,
        ),
    )

    if rows:
        rows[0]["is_top_waste_product"] = True

    return rows


def _build_ingredient_waste_rows(ingredient_snapshots):
    rows = []

    for snapshot in ingredient_snapshots:
        waste_rate_percent = _calculate_ingredient_waste_rate(snapshot)

        rows.append(
            {
                "snapshot": snapshot,
                "ingredient": snapshot.ingredient,
                "quantity_wasted": snapshot.quantity_wasted,
                "waste_cost": snapshot.waste_cost,
                "waste_rate_percent": waste_rate_percent,
                "recommended_action": _get_waste_ingredient_recommended_action(snapshot),
            }
        )

    return rows


def _build_waste_reason_rows(waste_records):
    grouped = {}

    for record in waste_records:
        reason = record.reason
        reason_label = record.get_reason_display()

        if reason not in grouped:
            grouped[reason] = {
                "reason": reason,
                "reason_label": reason_label,
                "record_count": 0,
                "total_cost": Decimal("0.00"),
                "recommended_action": _get_waste_reason_recommended_action(reason),
            }

        grouped[reason]["record_count"] += 1
        grouped[reason]["total_cost"] += record.estimated_cost or Decimal("0.00")

    return sorted(
        grouped.values(),
        key=lambda row: (
            -row["total_cost"],
            row["reason_label"],
        ),
    )


def _get_waste_product_recommended_action(snapshot):
    if snapshot.waste_cost > 0 and snapshot.action_flag == ProductPerformanceSnapshot.ACTION_REVIEW:
        return (
            "Review production quantity, recipe execution, pricing, and waste causes "
            "before promoting this product further."
        )

    if snapshot.waste_cost > 0:
        return (
            "Investigate waste records linked to this product and confirm whether "
            "batch planning or recipe control needs adjustment."
        )

    return (
        "No product-linked waste cost is currently recorded for this snapshot."
    )


def _get_waste_ingredient_recommended_action(snapshot):
    if snapshot.quantity_wasted > 0:
        return (
            "Review ingredient handling, expiry timing, and recipe execution to reduce "
            "avoidable waste."
        )

    return "No ingredient-linked waste action is required from this snapshot."


def _get_waste_reason_recommended_action(reason):
    action_map = {
        WasteRecord.REASON_OVERPRODUCTION: (
            "Review production planning and demand forecasting before the next batch."
        ),
        WasteRecord.REASON_QUALITY_ISSUE: (
            "Review recipe execution, preparation checks, and quality control steps."
        ),
        WasteRecord.REASON_EXPIRY: (
            "Review ingredient rotation, lot expiry visibility, and stock ordering rhythm."
        ),
        WasteRecord.REASON_RECIPE_ERROR: (
            "Review recipe instructions, staff process, and batch preparation controls."
        ),
        WasteRecord.REASON_DAMAGE: (
            "Review handling, storage, and transport steps to reduce damaged stock."
        ),
        WasteRecord.REASON_CANCELLATION: (
            "Review order confirmation timing and cancellation handling before production begins."
        ),
        WasteRecord.REASON_OTHER: (
            "Review the waste record notes and decide whether process controls need improvement."
        ),
    }

    return action_map.get(
        reason,
        "Review the waste record and decide whether process controls need improvement.",
    )
def occasion_analytics(request):
    latest_metric = (
        DailyBakeryMetric.objects.select_related("workspace")
        .order_by("-metric_date")
        .first()
    )

    workspace = latest_metric.workspace if latest_metric else None
    snapshot_date = latest_metric.metric_date if latest_metric else None

    occasion_snapshots = []
    occasion_rows = []
    top_occasion = None

    total_occasion_revenue = Decimal("0.00")
    total_occasion_orders = 0
    total_quantity_sold = 0
    total_upcoming_orders = 0
    total_delivery_pressure = 0

    if workspace and snapshot_date:
        occasion_snapshots = list(
            OccasionDemandSnapshot.objects.filter(
                workspace=workspace,
                snapshot_date=snapshot_date,
            )
            .select_related("occasion")
            .order_by("-revenue", "occasion__name")
        )

        total_occasion_revenue = sum(
            (snapshot.revenue for snapshot in occasion_snapshots),
            Decimal("0.00"),
        )
        total_occasion_orders = sum(
            snapshot.order_count for snapshot in occasion_snapshots
        )
        total_quantity_sold = sum(
            snapshot.quantity_sold for snapshot in occasion_snapshots
        )
        total_upcoming_orders = sum(
            snapshot.upcoming_order_count for snapshot in occasion_snapshots
        )
        total_delivery_pressure = sum(
            snapshot.delivery_slot_pressure_count for snapshot in occasion_snapshots
        )

        occasion_rows = _build_occasion_analytics_rows(
            occasion_snapshots=occasion_snapshots,
            total_revenue=total_occasion_revenue,
        )

        top_occasion = occasion_rows[0] if occasion_rows else None

    context = {
        "latest_metric": latest_metric,
        "workspace": workspace,
        "snapshot_date": snapshot_date,
        "occasion_rows": occasion_rows,
        "top_occasion": top_occasion,
        "occasion_count": len(occasion_snapshots),
        "total_occasion_revenue": total_occasion_revenue,
        "total_occasion_orders": total_occasion_orders,
        "total_quantity_sold": total_quantity_sold,
        "total_upcoming_orders": total_upcoming_orders,
        "total_delivery_pressure": total_delivery_pressure,
    }

    return render(request, "bakeops/occasion_analytics.html", context)


def customer_analytics(request):
    latest_metric = (
        DailyBakeryMetric.objects.select_related("workspace")
        .order_by("-metric_date")
        .first()
    )

    workspace = latest_metric.workspace if latest_metric else None
    snapshot_date = latest_metric.metric_date if latest_metric else None

    customer_snapshots = []
    customer_rows = []
    top_customer = None

    total_customer_revenue = Decimal("0.00")
    total_customer_orders = 0
    repeat_customer_count = 0
    total_loyalty_points_earned = 0
    total_current_points_balance = 0

    if workspace and snapshot_date:
        customer_snapshots = list(
            CustomerLoyaltySnapshot.objects.filter(
                workspace=workspace,
                snapshot_date=snapshot_date,
            )
            .select_related("customer")
            .order_by("-total_revenue", "customer__full_name")
        )

        total_customer_revenue = sum(
            (snapshot.total_revenue for snapshot in customer_snapshots),
            Decimal("0.00"),
        )
        total_customer_orders = sum(
            snapshot.total_orders for snapshot in customer_snapshots
        )
        repeat_customer_count = sum(
            1 for snapshot in customer_snapshots if snapshot.is_repeat_customer
        )
        total_loyalty_points_earned = sum(
            snapshot.loyalty_points_earned for snapshot in customer_snapshots
        )
        total_current_points_balance = sum(
            snapshot.current_points_balance for snapshot in customer_snapshots
        )

        customer_rows = _build_customer_analytics_rows(
            customer_snapshots=customer_snapshots,
            total_revenue=total_customer_revenue,
        )

        top_customer = customer_rows[0] if customer_rows else None

    context = {
        "latest_metric": latest_metric,
        "workspace": workspace,
        "snapshot_date": snapshot_date,
        "customer_rows": customer_rows,
        "top_customer": top_customer,
        "customer_count": len(customer_snapshots),
        "repeat_customer_count": repeat_customer_count,
        "new_customer_count": len(customer_snapshots) - repeat_customer_count,
        "total_customer_revenue": total_customer_revenue,
        "total_customer_orders": total_customer_orders,
        "total_loyalty_points_earned": total_loyalty_points_earned,
        "total_current_points_balance": total_current_points_balance,
    }

    return render(request, "bakeops/customer_analytics.html", context)


def _build_occasion_analytics_rows(occasion_snapshots, total_revenue):
    rows = []

    for snapshot in occasion_snapshots:
        revenue_share_percent = _calculate_share_percent(
            part=snapshot.revenue,
            total=total_revenue,
        )

        gross_margin_percent = _calculate_share_percent(
            part=snapshot.gross_margin,
            total=snapshot.revenue,
        )

        rows.append(
            {
                "snapshot": snapshot,
                "occasion": snapshot.occasion,
                "revenue_share_percent": revenue_share_percent,
                "gross_margin_percent": gross_margin_percent,
                "demand_label": _get_occasion_demand_label(snapshot),
                "demand_explanation": _get_occasion_demand_explanation(snapshot),
                "recommended_action": _get_occasion_recommended_action(snapshot),
                "has_delivery_pressure": snapshot.delivery_slot_pressure_count > 0,
                "has_upcoming_demand": snapshot.upcoming_order_count > 0,
            }
        )

    return sorted(
        rows,
        key=lambda row: (
            -row["snapshot"].revenue,
            -row["snapshot"].order_count,
            row["occasion"].name,
        ),
    )


def _build_customer_analytics_rows(customer_snapshots, total_revenue):
    rows = []

    for snapshot in customer_snapshots:
        revenue_share_percent = _calculate_share_percent(
            part=snapshot.total_revenue,
            total=total_revenue,
        )

        rows.append(
            {
                "snapshot": snapshot,
                "customer": snapshot.customer,
                "revenue_share_percent": revenue_share_percent,
                "customer_label": _get_customer_loyalty_label(snapshot),
                "customer_explanation": _get_customer_loyalty_explanation(snapshot),
                "recommended_action": _get_customer_recommended_action(snapshot),
            }
        )

    return sorted(
        rows,
        key=lambda row: (
            -row["snapshot"].total_revenue,
            -row["snapshot"].total_orders,
            row["customer"].full_name,
        ),
    )


def _calculate_share_percent(part, total):
    part = part or Decimal("0.00")
    total = total or Decimal("0.00")

    if total <= 0:
        return Decimal("0.00")

    return ((part / total) * Decimal("100")).quantize(Decimal("0.01"))


def _get_occasion_demand_label(snapshot):
    if snapshot.delivery_slot_pressure_count > 0:
        return "Capacity pressure"

    if snapshot.upcoming_order_count > 0 and snapshot.revenue > 0:
        return "Active demand"

    if snapshot.upcoming_order_count > 0:
        return "Upcoming demand"

    if snapshot.revenue > 0:
        return "Historical demand"

    return "Monitor"


def _get_occasion_demand_explanation(snapshot):
    if snapshot.delivery_slot_pressure_count > 0:
        return (
            "This occasion has delivery-slot pressure, so planning capacity and "
            "production timing need review."
        )

    if snapshot.upcoming_order_count > 0 and snapshot.revenue > 0:
        return (
            "This occasion has both existing revenue and upcoming demand, making it "
            "important for near-term planning."
        )

    if snapshot.upcoming_order_count > 0:
        return (
            "This occasion has upcoming demand even though recent revenue is low or zero."
        )

    if snapshot.revenue > 0:
        return (
            "This occasion generated revenue in the latest snapshot period."
        )

    return (
        "This occasion currently has low activity but should remain visible for future demand."
    )


def _get_occasion_recommended_action(snapshot):
    if snapshot.delivery_slot_pressure_count > 0:
        return (
            "Review production slots, delivery planning, and staffing before accepting "
            "additional orders for this occasion."
        )

    if snapshot.upcoming_order_count > 0:
        return (
            "Check ingredient availability and batch planning for upcoming orders."
        )

    if snapshot.revenue > 0:
        return (
            "Monitor product mix and margin performance for this occasion."
        )

    return (
        "Keep this occasion available for tracking, but no immediate action is required."
    )


def _get_customer_loyalty_label(snapshot):
    if snapshot.is_repeat_customer and snapshot.total_revenue >= Decimal("250.00"):
        return "High-value repeat"

    if snapshot.is_repeat_customer:
        return "Repeat customer"

    if snapshot.total_orders == 1:
        return "New / one-time customer"

    return "Monitor"


def _get_customer_loyalty_explanation(snapshot):
    if snapshot.is_repeat_customer and snapshot.total_revenue >= Decimal("250.00"):
        return (
            "This customer has repeat behaviour and high revenue contribution."
        )

    if snapshot.is_repeat_customer:
        return (
            "This customer has repeat behaviour and should be tracked for loyalty value."
        )

    if snapshot.total_orders == 1:
        return (
            "This customer has one recorded order in the current snapshot."
        )

    return (
        "This customer should remain visible for future order and loyalty tracking."
    )


def _get_customer_recommended_action(snapshot):
    if snapshot.is_repeat_customer and snapshot.current_points_balance >= 100:
        return (
            "Review loyalty balance and consider whether the customer may be close to "
            "a future reward or retention opportunity."
        )

    if snapshot.is_repeat_customer:
        return (
            "Monitor repeat purchase behaviour and average order value."
        )

    if snapshot.total_orders == 1:
        return (
            "Track whether this customer places another order before treating them as loyal."
        )

    return (
        "Continue monitoring customer value after the next metric build."
    )

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