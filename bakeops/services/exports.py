import csv
from pathlib import Path

from django.conf import settings

from bakeops.models import (
    BakeryOrder,
    BakeryOrderItem,
    DailyBakeryMetric,
    Ingredient,
    OccasionType,
    ProductPerformanceSnapshot,
    ProductionBatch,
    ProductionBatchLine,
    WasteRecord,
    Workspace,
)
from cakes.models import Cake, CakeCollection, CakeVariant


EXPORT_FILE_NAMES = {
    "fact_orders": "fact_orders.csv",
    "fact_order_items": "fact_order_items.csv",
    "fact_waste": "fact_waste.csv",
    "fact_production_batches": "fact_production_batches.csv",
    "dim_cake": "dim_cake.csv",
    "dim_ingredient": "dim_ingredient.csv",
    "dim_customer": "dim_customer.csv",
    "dim_occasion": "dim_occasion.csv",
    "dim_collection": "dim_collection.csv",
    "daily_bakery_metrics": "daily_bakery_metrics.csv",
    "product_performance_snapshot": "product_performance_snapshot.csv",
}


def export_bi_csv(workspace=None, output_dir=None):
    """
    Export BakeOps V1 BI-ready CSV files.

    The export contract is intentionally stable:
    - facts are event/transaction-like tables
    - dimensions are descriptive lookup tables
    - gold-layer exports mirror dashboard snapshot tables
    """

    workspace = workspace or Workspace.objects.filter(is_active=True).first()

    if workspace is None:
        raise ValueError("No active workspace found. Run seed_demo_data first.")

    output_path = Path(output_dir or settings.BASE_DIR / "exports")
    output_path.mkdir(parents=True, exist_ok=True)

    exports = [
        _export_fact_orders(workspace, output_path),
        _export_fact_order_items(workspace, output_path),
        _export_fact_waste(workspace, output_path),
        _export_fact_production_batches(workspace, output_path),
        _export_dim_cake(output_path),
        _export_dim_ingredient(workspace, output_path),
        _export_dim_customer(workspace, output_path),
        _export_dim_occasion(workspace, output_path),
        _export_dim_collection(output_path),
        _export_daily_bakery_metrics(workspace, output_path),
        _export_product_performance_snapshot(workspace, output_path),
    ]

    return {
        "workspace": workspace.name,
        "output_dir": str(output_path),
        "files": exports,
        "file_count": len(exports),
        "row_count": sum(item["rows"] for item in exports),
    }


def _write_csv(path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            writer.writerow(row)

    return {
        "file": path.name,
        "path": str(path),
        "rows": len(rows),
        "columns": len(fieldnames),
    }


def _export_fact_orders(workspace, output_path):
    fieldnames = [
        "order_id",
        "workspace_id",
        "workspace_name",
        "order_number",
        "customer_id",
        "occasion_id",
        "delivery_slot_id",
        "order_date",
        "required_date",
        "status",
        "channel",
        "subtotal",
        "discount_amount",
        "total_amount",
        "loyalty_points_earned",
        "loyalty_points_redeemed",
    ]

    rows = []

    orders = (
        BakeryOrder.objects.filter(workspace=workspace)
        .select_related("workspace", "customer", "occasion", "delivery_slot")
        .order_by("order_date", "order_number")
    )

    for order in orders:
        rows.append(
            {
                "order_id": order.id,
                "workspace_id": order.workspace_id,
                "workspace_name": order.workspace.name,
                "order_number": order.order_number,
                "customer_id": order.customer_id or "",
                "occasion_id": order.occasion_id or "",
                "delivery_slot_id": order.delivery_slot_id or "",
                "order_date": order.order_date,
                "required_date": order.required_date or "",
                "status": order.status,
                "channel": order.channel,
                "subtotal": order.subtotal,
                "discount_amount": order.discount_amount,
                "total_amount": order.total_amount,
                "loyalty_points_earned": order.loyalty_points_earned,
                "loyalty_points_redeemed": order.loyalty_points_redeemed,
            }
        )

    return _write_csv(
        output_path / EXPORT_FILE_NAMES["fact_orders"],
        fieldnames,
        rows,
    )


def _export_fact_order_items(workspace, output_path):
    fieldnames = [
        "order_item_id",
        "order_id",
        "order_number",
        "workspace_id",
        "cake_id",
        "cake_name",
        "variant_id",
        "variant_label",
        "quantity",
        "unit_price",
        "line_total",
    ]

    rows = []

    items = (
        BakeryOrderItem.objects.filter(order__workspace=workspace)
        .select_related("order", "cake", "variant")
        .order_by("order__order_date", "order__order_number", "cake__name")
    )

    for item in items:
        rows.append(
            {
                "order_item_id": item.id,
                "order_id": item.order_id,
                "order_number": item.order.order_number,
                "workspace_id": item.order.workspace_id,
                "cake_id": item.cake_id,
                "cake_name": item.cake.name,
                "variant_id": item.variant_id or "",
                "variant_label": item.variant.label if item.variant else "",
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "line_total": item.line_total,
            }
        )

    return _write_csv(
        output_path / EXPORT_FILE_NAMES["fact_order_items"],
        fieldnames,
        rows,
    )


def _export_fact_waste(workspace, output_path):
    fieldnames = [
        "waste_id",
        "workspace_id",
        "waste_date",
        "reason",
        "ingredient_id",
        "ingredient_name",
        "cake_id",
        "cake_name",
        "variant_id",
        "variant_label",
        "batch_line_id",
        "quantity",
        "estimated_cost",
        "notes",
    ]

    rows = []

    waste_records = (
        WasteRecord.objects.filter(workspace=workspace)
        .select_related("ingredient", "cake", "variant", "batch_line")
        .order_by("waste_date", "reason")
    )

    for waste in waste_records:
        rows.append(
            {
                "waste_id": waste.id,
                "workspace_id": waste.workspace_id,
                "waste_date": waste.waste_date,
                "reason": waste.reason,
                "ingredient_id": waste.ingredient_id or "",
                "ingredient_name": waste.ingredient.name if waste.ingredient else "",
                "cake_id": waste.cake_id or "",
                "cake_name": waste.cake.name if waste.cake else "",
                "variant_id": waste.variant_id or "",
                "variant_label": waste.variant.label if waste.variant else "",
                "batch_line_id": waste.batch_line_id or "",
                "quantity": waste.quantity,
                "estimated_cost": waste.estimated_cost,
                "notes": waste.notes,
            }
        )

    return _write_csv(
        output_path / EXPORT_FILE_NAMES["fact_waste"],
        fieldnames,
        rows,
    )


def _export_fact_production_batches(workspace, output_path):
    fieldnames = [
        "production_batch_id",
        "production_batch_line_id",
        "workspace_id",
        "batch_code",
        "production_date",
        "status",
        "recipe_id",
        "recipe_name",
        "cake_id",
        "cake_name",
        "variant_id",
        "variant_label",
        "planned_quantity",
        "produced_quantity",
        "failed_quantity",
    ]

    rows = []

    batch_lines = (
        ProductionBatchLine.objects.filter(batch__workspace=workspace)
        .select_related("batch", "recipe", "recipe__cake", "recipe__variant")
        .order_by("batch__production_date", "batch__batch_code", "recipe__name")
    )

    for line in batch_lines:
        rows.append(
            {
                "production_batch_id": line.batch_id,
                "production_batch_line_id": line.id,
                "workspace_id": line.batch.workspace_id,
                "batch_code": line.batch.batch_code,
                "production_date": line.batch.production_date,
                "status": line.batch.status,
                "recipe_id": line.recipe_id,
                "recipe_name": line.recipe.name,
                "cake_id": line.recipe.cake_id,
                "cake_name": line.recipe.cake.name,
                "variant_id": line.recipe.variant_id or "",
                "variant_label": line.recipe.variant.label if line.recipe.variant else "",
                "planned_quantity": line.planned_quantity,
                "produced_quantity": line.produced_quantity,
                "failed_quantity": line.failed_quantity,
            }
        )

    return _write_csv(
        output_path / EXPORT_FILE_NAMES["fact_production_batches"],
        fieldnames,
        rows,
    )


def _export_dim_cake(output_path):
    fieldnames = [
        "cake_id",
        "cake_name",
        "slug",
        "code",
        "category",
        "occasion_type",
        "is_active",
        "variant_id",
        "variant_label",
        "serves_min",
        "serves_max",
        "price",
        "is_default_variant",
    ]

    rows = []

    variants = (
        CakeVariant.objects.select_related("cake")
        .filter(cake__slug__startswith="demo-")
        .order_by("cake__name", "label")
    )

    for variant in variants:
        rows.append(
            {
                "cake_id": variant.cake_id,
                "cake_name": variant.cake.name,
                "slug": variant.cake.slug,
                "code": variant.cake.code,
                "category": variant.cake.category,
                "occasion_type": variant.cake.occasion_type,
                "is_active": variant.cake.is_active,
                "variant_id": variant.id,
                "variant_label": variant.label,
                "serves_min": variant.serves_min,
                "serves_max": variant.serves_max,
                "price": variant.price,
                "is_default_variant": variant.is_default,
            }
        )

    return _write_csv(
        output_path / EXPORT_FILE_NAMES["dim_cake"],
        fieldnames,
        rows,
    )


def _export_dim_ingredient(workspace, output_path):
    fieldnames = [
        "ingredient_id",
        "workspace_id",
        "ingredient_name",
        "supplier_id",
        "supplier_name",
        "unit",
        "cost_per_unit",
        "current_stock_quantity",
        "reorder_level_quantity",
        "is_active",
    ]

    rows = []

    ingredients = (
        Ingredient.objects.filter(workspace=workspace)
        .select_related("supplier")
        .order_by("name")
    )

    for ingredient in ingredients:
        rows.append(
            {
                "ingredient_id": ingredient.id,
                "workspace_id": ingredient.workspace_id,
                "ingredient_name": ingredient.name,
                "supplier_id": ingredient.supplier_id or "",
                "supplier_name": ingredient.supplier.name if ingredient.supplier else "",
                "unit": ingredient.unit,
                "cost_per_unit": ingredient.cost_per_unit,
                "current_stock_quantity": ingredient.current_stock_quantity,
                "reorder_level_quantity": ingredient.reorder_level_quantity,
                "is_active": ingredient.is_active,
            }
        )

    return _write_csv(
        output_path / EXPORT_FILE_NAMES["dim_ingredient"],
        fieldnames,
        rows,
    )


def _export_dim_customer(workspace, output_path):
    fieldnames = [
        "customer_id",
        "workspace_id",
        "full_name",
        "email",
        "phone",
        "postcode",
        "is_repeat_customer",
        "points_balance",
        "lifetime_points_earned",
        "lifetime_points_redeemed",
    ]

    rows = []

    customers = workspace.customers.prefetch_related("bakeops_loyalty_account").order_by(
        "full_name"
    )

    for customer in customers:
        loyalty = getattr(customer, "bakeops_loyalty_account", None)

        rows.append(
            {
                "customer_id": customer.id,
                "workspace_id": customer.workspace_id,
                "full_name": customer.full_name,
                "email": customer.email,
                "phone": customer.phone,
                "postcode": customer.postcode,
                "is_repeat_customer": customer.is_repeat_customer,
                "points_balance": loyalty.points_balance if loyalty else 0,
                "lifetime_points_earned": loyalty.lifetime_points_earned if loyalty else 0,
                "lifetime_points_redeemed": loyalty.lifetime_points_redeemed if loyalty else 0,
            }
        )

    return _write_csv(
        output_path / EXPORT_FILE_NAMES["dim_customer"],
        fieldnames,
        rows,
    )


def _export_dim_occasion(workspace, output_path):
    fieldnames = [
        "occasion_id",
        "workspace_id",
        "occasion_name",
        "description",
        "is_active",
    ]

    rows = []

    occasions = OccasionType.objects.filter(workspace=workspace).order_by("name")

    for occasion in occasions:
        rows.append(
            {
                "occasion_id": occasion.id,
                "workspace_id": occasion.workspace_id,
                "occasion_name": occasion.name,
                "description": occasion.description,
                "is_active": occasion.is_active,
            }
        )

    return _write_csv(
        output_path / EXPORT_FILE_NAMES["dim_occasion"],
        fieldnames,
        rows,
    )


def _export_dim_collection(output_path):
    fieldnames = [
        "collection_id",
        "key",
        "label",
        "icon",
        "description",
        "is_active",
        "sort_order",
    ]

    rows = []

    collections = CakeCollection.objects.filter(key__startswith="demo-").order_by(
        "sort_order",
        "label",
    )

    for collection in collections:
        rows.append(
            {
                "collection_id": collection.id,
                "key": collection.key,
                "label": collection.label,
                "icon": collection.icon,
                "description": collection.description,
                "is_active": collection.is_active,
                "sort_order": collection.sort_order,
            }
        )

    return _write_csv(
        output_path / EXPORT_FILE_NAMES["dim_collection"],
        fieldnames,
        rows,
    )


def _export_daily_bakery_metrics(workspace, output_path):
    fieldnames = [
        "metric_id",
        "workspace_id",
        "metric_date",
        "revenue",
        "paid_orders",
        "average_order_value",
        "total_items_sold",
        "ingredient_cost",
        "gross_margin",
        "gross_margin_percent",
        "waste_cost",
        "waste_adjusted_margin",
        "waste_adjusted_margin_percent",
    ]

    rows = []

    metrics = DailyBakeryMetric.objects.filter(workspace=workspace).order_by(
        "metric_date"
    )

    for metric in metrics:
        rows.append(
            {
                "metric_id": metric.id,
                "workspace_id": metric.workspace_id,
                "metric_date": metric.metric_date,
                "revenue": metric.revenue,
                "paid_orders": metric.paid_orders,
                "average_order_value": metric.average_order_value,
                "total_items_sold": metric.total_items_sold,
                "ingredient_cost": metric.ingredient_cost,
                "gross_margin": metric.gross_margin,
                "gross_margin_percent": metric.gross_margin_percent,
                "waste_cost": metric.waste_cost,
                "waste_adjusted_margin": metric.waste_adjusted_margin,
                "waste_adjusted_margin_percent": metric.waste_adjusted_margin_percent,
            }
        )

    return _write_csv(
        output_path / EXPORT_FILE_NAMES["daily_bakery_metrics"],
        fieldnames,
        rows,
    )


def _export_product_performance_snapshot(workspace, output_path):
    fieldnames = [
        "snapshot_id",
        "workspace_id",
        "snapshot_date",
        "cake_id",
        "cake_name",
        "variant_id",
        "variant_label",
        "revenue",
        "quantity_sold",
        "paid_order_count",
        "ingredient_cost",
        "gross_margin",
        "gross_margin_percent",
        "waste_cost",
        "waste_adjusted_margin",
        "waste_adjusted_margin_percent",
        "revenue_rank",
        "waste_adjusted_margin_rank",
        "action_flag",
        "action_reason",
    ]

    rows = []

    snapshots = (
        ProductPerformanceSnapshot.objects.filter(workspace=workspace)
        .select_related("cake", "variant")
        .order_by("snapshot_date", "revenue_rank", "cake__name")
    )

    for snapshot in snapshots:
        rows.append(
            {
                "snapshot_id": snapshot.id,
                "workspace_id": snapshot.workspace_id,
                "snapshot_date": snapshot.snapshot_date,
                "cake_id": snapshot.cake_id,
                "cake_name": snapshot.cake.name,
                "variant_id": snapshot.variant_id or "",
                "variant_label": snapshot.variant.label if snapshot.variant else "",
                "revenue": snapshot.revenue,
                "quantity_sold": snapshot.quantity_sold,
                "paid_order_count": snapshot.paid_order_count,
                "ingredient_cost": snapshot.ingredient_cost,
                "gross_margin": snapshot.gross_margin,
                "gross_margin_percent": snapshot.gross_margin_percent,
                "waste_cost": snapshot.waste_cost,
                "waste_adjusted_margin": snapshot.waste_adjusted_margin,
                "waste_adjusted_margin_percent": snapshot.waste_adjusted_margin_percent,
                "revenue_rank": snapshot.revenue_rank,
                "waste_adjusted_margin_rank": snapshot.waste_adjusted_margin_rank,
                "action_flag": snapshot.action_flag,
                "action_reason": snapshot.action_reason,
            }
        )

    return _write_csv(
        output_path / EXPORT_FILE_NAMES["product_performance_snapshot"],
        fieldnames,
        rows,
    )