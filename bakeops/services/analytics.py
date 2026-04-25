from collections import defaultdict
from datetime import date
from decimal import Decimal

from django.db import transaction
from django.db.models import Sum

from bakeops.models import (
    BakeryOrder,
    BakeryOrderItem,
    Customer,
    CustomerLoyaltySnapshot,
    DailyBakeryMetric,
    Ingredient,
    IngredientUsageSnapshot,
    LoyaltyAccount,
    OccasionDemandSnapshot,
    OccasionType,
    ProductPerformanceSnapshot,
    WasteRecord,
    Workspace,
)

from .costing import (
    calculate_order_ingredient_cost,
    calculate_order_item_ingredient_cost,
    get_recipe_for_order_item,
    money,
    safe_percent,
)
from .quality import rebuild_data_quality_issues


PAID_STATUSES = [
    BakeryOrder.STATUS_PAID,
    BakeryOrder.STATUS_FULFILLED,
]


@transaction.atomic
def build_bakery_metrics(workspace=None, snapshot_date=None):
    snapshot_date = snapshot_date or date.today()

    if workspace is not None:
        workspaces = Workspace.objects.filter(pk=workspace.pk)
    else:
        workspaces = Workspace.objects.filter(is_active=True)

    summary = {
        "workspaces_processed": 0,
        "rows_processed": 0,
        "metrics_created": 0,
        "snapshots_created": 0,
        "issues_created": 0,
    }

    for current_workspace in workspaces:
        workspace_summary = _build_workspace_metrics(current_workspace, snapshot_date)

        summary["workspaces_processed"] += 1
        summary["rows_processed"] += workspace_summary["rows_processed"]
        summary["metrics_created"] += workspace_summary["metrics_created"]
        summary["snapshots_created"] += workspace_summary["snapshots_created"]
        summary["issues_created"] += workspace_summary["issues_created"]

    return summary


def _build_workspace_metrics(workspace, snapshot_date):
    _clear_existing_snapshots(workspace, snapshot_date)

    paid_orders = BakeryOrder.objects.filter(
        workspace=workspace,
        status__in=PAID_STATUSES,
    ).select_related("customer", "occasion", "delivery_slot")

    paid_items = BakeryOrderItem.objects.filter(
        order__workspace=workspace,
        order__status__in=PAID_STATUSES,
    ).select_related("order", "cake", "variant")

    product_summary = _build_product_performance_snapshots(
        workspace=workspace,
        snapshot_date=snapshot_date,
        paid_items=paid_items,
    )

    daily_metric = _build_daily_metric(
        workspace=workspace,
        snapshot_date=snapshot_date,
        paid_orders=paid_orders,
        paid_items=paid_items,
        product_summary=product_summary,
    )

    ingredient_count = _build_ingredient_usage_snapshots(
        workspace=workspace,
        snapshot_date=snapshot_date,
        paid_items=paid_items,
    )

    occasion_count = _build_occasion_demand_snapshots(
        workspace=workspace,
        snapshot_date=snapshot_date,
        paid_orders=paid_orders,
    )

    customer_count = _build_customer_loyalty_snapshots(
        workspace=workspace,
        snapshot_date=snapshot_date,
        paid_orders=paid_orders,
    )

    issues_created = rebuild_data_quality_issues(workspace, snapshot_date)

    return {
        "rows_processed": paid_orders.count() + paid_items.count(),
        "metrics_created": 1 if daily_metric else 0,
        "snapshots_created": (
            product_summary["created_count"]
            + ingredient_count
            + occasion_count
            + customer_count
        ),
        "issues_created": issues_created,
    }


def _clear_existing_snapshots(workspace, snapshot_date):
    ProductPerformanceSnapshot.objects.filter(
        workspace=workspace,
        snapshot_date=snapshot_date,
    ).delete()

    IngredientUsageSnapshot.objects.filter(
        workspace=workspace,
        snapshot_date=snapshot_date,
    ).delete()

    OccasionDemandSnapshot.objects.filter(
        workspace=workspace,
        snapshot_date=snapshot_date,
    ).delete()

    CustomerLoyaltySnapshot.objects.filter(
        workspace=workspace,
        snapshot_date=snapshot_date,
    ).delete()


def _build_product_performance_snapshots(workspace, snapshot_date, paid_items):
    grouped = defaultdict(
        lambda: {
            "cake": None,
            "variant": None,
            "revenue": Decimal("0.00"),
            "quantity_sold": 0,
            "order_ids": set(),
            "ingredient_cost": Decimal("0.00"),
            "waste_cost": Decimal("0.00"),
        }
    )

    for item in paid_items:
        key = (item.cake_id, item.variant_id)

        grouped[key]["cake"] = item.cake
        grouped[key]["variant"] = item.variant
        grouped[key]["revenue"] += Decimal(item.line_total or 0)
        grouped[key]["quantity_sold"] += item.quantity or 0
        grouped[key]["order_ids"].add(item.order_id)
        grouped[key]["ingredient_cost"] += calculate_order_item_ingredient_cost(item)

    waste_records = WasteRecord.objects.filter(workspace=workspace).select_related(
        "cake",
        "variant",
    )

    for waste_record in waste_records:
        if not waste_record.cake_id:
            continue

        key = (waste_record.cake_id, waste_record.variant_id)

        if key in grouped:
            grouped[key]["waste_cost"] += Decimal(waste_record.estimated_cost or 0)

    rows = []

    for key, row in grouped.items():
        revenue = money(row["revenue"])
        ingredient_cost = money(row["ingredient_cost"])
        waste_cost = money(row["waste_cost"])

        gross_margin = money(revenue - ingredient_cost)
        gross_margin_percent = safe_percent(gross_margin, revenue)

        waste_adjusted_margin = money(gross_margin - waste_cost)
        waste_adjusted_margin_percent = safe_percent(waste_adjusted_margin, revenue)

        rows.append(
            {
                "key": key,
                "cake": row["cake"],
                "variant": row["variant"],
                "revenue": revenue,
                "quantity_sold": row["quantity_sold"],
                "paid_order_count": len(row["order_ids"]),
                "ingredient_cost": ingredient_cost,
                "gross_margin": gross_margin,
                "gross_margin_percent": gross_margin_percent,
                "waste_cost": waste_cost,
                "waste_adjusted_margin": waste_adjusted_margin,
                "waste_adjusted_margin_percent": waste_adjusted_margin_percent,
            }
        )

    revenue_ranked = sorted(
        rows,
        key=lambda item: item["revenue"],
        reverse=True,
    )

    margin_ranked = sorted(
        rows,
        key=lambda item: (
            item["waste_adjusted_margin_percent"],
            item["waste_adjusted_margin"],
        ),
        reverse=True,
    )

    revenue_ranks = {
        row["key"]: index + 1
        for index, row in enumerate(revenue_ranked)
    }

    margin_ranks = {
        row["key"]: index + 1
        for index, row in enumerate(margin_ranked)
    }

    created_count = 0

    for row in rows:
        revenue_rank = revenue_ranks[row["key"]]
        margin_rank = margin_ranks[row["key"]]

        action_flag, action_reason = _get_product_action(
            revenue_rank=revenue_rank,
            margin_rank=margin_rank,
            row=row,
        )

        ProductPerformanceSnapshot.objects.create(
            workspace=workspace,
            snapshot_date=snapshot_date,
            cake=row["cake"],
            variant=row["variant"],
            revenue=row["revenue"],
            quantity_sold=row["quantity_sold"],
            paid_order_count=row["paid_order_count"],
            ingredient_cost=row["ingredient_cost"],
            gross_margin=row["gross_margin"],
            gross_margin_percent=row["gross_margin_percent"],
            waste_cost=row["waste_cost"],
            waste_adjusted_margin=row["waste_adjusted_margin"],
            waste_adjusted_margin_percent=row["waste_adjusted_margin_percent"],
            revenue_rank=revenue_rank,
            waste_adjusted_margin_rank=margin_rank,
            action_flag=action_flag,
            action_reason=action_reason,
        )
        created_count += 1

    return {
        "rows": rows,
        "created_count": created_count,
    }


def _get_product_action(revenue_rank, margin_rank, row):
    if revenue_rank == 1 and margin_rank > revenue_rank:
        return (
            ProductPerformanceSnapshot.ACTION_REVIEW,
            "This product sells strongly, but waste-adjusted margin rank is weaker than revenue rank.",
        )

    if margin_rank <= 2 and revenue_rank > margin_rank:
        return (
            ProductPerformanceSnapshot.ACTION_PROMOTE,
            "This product has stronger waste-adjusted margin performance than revenue ranking suggests.",
        )

    if margin_rank >= 4:
        return (
            ProductPerformanceSnapshot.ACTION_REDUCE,
            "This product has weak waste-adjusted margin performance and should be reviewed.",
        )

    return (
        ProductPerformanceSnapshot.ACTION_STABLE,
        "This product has stable revenue and margin performance.",
    )


def _build_daily_metric(workspace, snapshot_date, paid_orders, paid_items, product_summary):
    revenue = money(sum((Decimal(order.total_amount or 0) for order in paid_orders), Decimal("0.00")))
    paid_order_count = paid_orders.count()
    total_items_sold = sum((item.quantity or 0 for item in paid_items), 0)

    ingredient_cost = money(
        sum(
            (row["ingredient_cost"] for row in product_summary["rows"]),
            Decimal("0.00"),
        )
    )

    waste_cost = money(
        WasteRecord.objects.filter(workspace=workspace).aggregate(
            total=Sum("estimated_cost")
        )["total"]
        or Decimal("0.00")
    )

    gross_margin = money(revenue - ingredient_cost)
    gross_margin_percent = safe_percent(gross_margin, revenue)

    waste_adjusted_margin = money(gross_margin - waste_cost)
    waste_adjusted_margin_percent = safe_percent(waste_adjusted_margin, revenue)

    average_order_value = money(revenue / paid_order_count) if paid_order_count else Decimal("0.00")

    metric, _ = DailyBakeryMetric.objects.update_or_create(
        workspace=workspace,
        metric_date=snapshot_date,
        defaults={
            "revenue": revenue,
            "paid_orders": paid_order_count,
            "average_order_value": average_order_value,
            "total_items_sold": total_items_sold,
            "ingredient_cost": ingredient_cost,
            "gross_margin": gross_margin,
            "gross_margin_percent": gross_margin_percent,
            "waste_cost": waste_cost,
            "waste_adjusted_margin": waste_adjusted_margin,
            "waste_adjusted_margin_percent": waste_adjusted_margin_percent,
        },
    )

    return metric


def _build_ingredient_usage_snapshots(workspace, snapshot_date, paid_items):
    ingredient_rows = defaultdict(
        lambda: {
            "quantity_used": Decimal("0.000"),
            "quantity_wasted": Decimal("0.000"),
            "ingredient_cost": Decimal("0.00"),
            "waste_cost": Decimal("0.00"),
        }
    )

    for item in paid_items:
        recipe = get_recipe_for_order_item(item)

        if recipe is None:
            continue

        for line in recipe.lines.select_related("ingredient").all():
            ingredient = line.ingredient
            quantity_used = Decimal(line.quantity_required or 0) * Decimal(item.quantity or 0)
            ingredient_rows[ingredient.pk]["quantity_used"] += quantity_used
            ingredient_rows[ingredient.pk]["ingredient_cost"] += (
                quantity_used * Decimal(ingredient.cost_per_unit or 0)
            )

    for waste in WasteRecord.objects.filter(workspace=workspace).select_related("ingredient"):
        if not waste.ingredient_id:
            continue

        ingredient_rows[waste.ingredient_id]["quantity_wasted"] += Decimal(waste.quantity or 0)
        ingredient_rows[waste.ingredient_id]["waste_cost"] += Decimal(waste.estimated_cost or 0)

    created_count = 0

    for ingredient in Ingredient.objects.filter(workspace=workspace):
        row = ingredient_rows[ingredient.pk]

        near_expiry_lots = ingredient.lots.filter(
            expiry_date__isnull=False,
            expiry_date__lte=snapshot_date,
            quantity_remaining__gt=Decimal("0.000"),
        )

        future_expiry_lots = ingredient.lots.filter(
            expiry_date__isnull=False,
            quantity_remaining__gt=Decimal("0.000"),
        ).order_by("expiry_date")

        nearest_lot = future_expiry_lots.first()

        stock_risk_level = _get_stock_risk_level(
            ingredient=ingredient,
            near_expiry_lot_count=near_expiry_lots.count(),
        )

        IngredientUsageSnapshot.objects.create(
            workspace=workspace,
            snapshot_date=snapshot_date,
            ingredient=ingredient,
            quantity_used=row["quantity_used"],
            quantity_wasted=row["quantity_wasted"],
            ingredient_cost=money(row["ingredient_cost"]),
            waste_cost=money(row["waste_cost"]),
            current_stock_quantity=ingredient.current_stock_quantity,
            reorder_level_quantity=ingredient.reorder_level_quantity,
            stock_risk_level=stock_risk_level,
            near_expiry_lot_count=near_expiry_lots.count(),
            nearest_expiry_date=nearest_lot.expiry_date if nearest_lot else None,
        )
        created_count += 1

    return created_count


def _get_stock_risk_level(ingredient, near_expiry_lot_count):
    if ingredient.current_stock_quantity <= 0:
        return IngredientUsageSnapshot.RISK_CRITICAL

    if ingredient.current_stock_quantity <= ingredient.reorder_level_quantity:
        return IngredientUsageSnapshot.RISK_HIGH

    if near_expiry_lot_count > 0:
        return IngredientUsageSnapshot.RISK_MEDIUM

    return IngredientUsageSnapshot.RISK_LOW


def _build_occasion_demand_snapshots(workspace, snapshot_date, paid_orders):
    created_count = 0

    for occasion in OccasionType.objects.filter(workspace=workspace):
        occasion_orders = paid_orders.filter(occasion=occasion)

        revenue = money(
            sum(
                (Decimal(order.total_amount or 0) for order in occasion_orders),
                Decimal("0.00"),
            )
        )

        quantity_sold = 0
        ingredient_cost = Decimal("0.00")

        for order in occasion_orders:
            quantity_sold += sum((item.quantity or 0 for item in order.items.all()), 0)
            ingredient_cost += calculate_order_ingredient_cost(order)

        gross_margin = money(revenue - ingredient_cost)

        upcoming_orders = BakeryOrder.objects.filter(
            workspace=workspace,
            occasion=occasion,
            required_date__gte=snapshot_date,
            status__in=[
                BakeryOrder.STATUS_DRAFT,
                BakeryOrder.STATUS_CONFIRMED,
                BakeryOrder.STATUS_PAID,
            ],
        )

        pressure_count = 0

        for order in upcoming_orders.select_related("delivery_slot"):
            slot = order.delivery_slot

            if slot and slot.capacity_orders and slot.booked_orders >= (slot.capacity_orders - 2):
                pressure_count += 1

        OccasionDemandSnapshot.objects.create(
            workspace=workspace,
            snapshot_date=snapshot_date,
            occasion=occasion,
            order_count=occasion_orders.count(),
            quantity_sold=quantity_sold,
            revenue=revenue,
            gross_margin=gross_margin,
            upcoming_order_count=upcoming_orders.count(),
            delivery_slot_pressure_count=pressure_count,
        )
        created_count += 1

    return created_count


def _build_customer_loyalty_snapshots(workspace, snapshot_date, paid_orders):
    created_count = 0

    for customer in Customer.objects.filter(workspace=workspace):
        customer_orders = paid_orders.filter(customer=customer)

        revenue = money(
            sum(
                (Decimal(order.total_amount or 0) for order in customer_orders),
                Decimal("0.00"),
            )
        )

        order_count = customer_orders.count()
        average_order_value = money(revenue / order_count) if order_count else Decimal("0.00")

        points_earned = sum((order.loyalty_points_earned or 0 for order in customer_orders), 0)
        points_redeemed = sum((order.loyalty_points_redeemed or 0 for order in customer_orders), 0)

        loyalty_account = LoyaltyAccount.objects.filter(
            workspace=workspace,
            customer=customer,
        ).first()

        CustomerLoyaltySnapshot.objects.create(
            workspace=workspace,
            snapshot_date=snapshot_date,
            customer=customer,
            total_orders=order_count,
            total_revenue=revenue,
            average_order_value=average_order_value,
            loyalty_points_earned=points_earned,
            loyalty_points_redeemed=points_redeemed,
            current_points_balance=loyalty_account.points_balance if loyalty_account else 0,
            is_repeat_customer=order_count > 1 or customer.is_repeat_customer,
        )
        created_count += 1

    return created_count