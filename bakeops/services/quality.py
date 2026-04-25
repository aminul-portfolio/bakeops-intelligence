from datetime import timedelta
from decimal import Decimal

from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum

from bakeops.models import (
    BakeryOrder,
    DataQualityIssue,
    Ingredient,
    IngredientLot,
    ProductionBatchLine,
    Recipe,
    WasteRecord,
)
from cakes.models import Cake, CakeVariant


def rebuild_data_quality_issues(workspace, snapshot_date):
    DataQualityIssue.objects.filter(workspace=workspace).delete()

    created = 0

    created += _check_active_cakes_without_variants(workspace)
    created += _check_variants_without_recipes(workspace)
    created += _check_recipes_without_lines(workspace)
    created += _check_paid_orders_without_items(workspace)
    created += _check_zero_total_orders(workspace)
    created += _check_low_stock_ingredients(workspace)
    created += _check_near_expiry_lots(workspace, snapshot_date)
    created += _check_waste_without_reason(workspace)
    created += _check_production_under_target(workspace)
    created += _check_unallocated_production(workspace)

    return created


def _create_issue(
    *,
    workspace,
    issue_type,
    severity,
    title,
    description="",
    suggested_action="",
    affected_object=None,
):
    content_type = None
    object_id = None

    if affected_object is not None:
        content_type = ContentType.objects.get_for_model(
            affected_object,
            for_concrete_model=False,
        )
        object_id = affected_object.pk

    DataQualityIssue.objects.create(
        workspace=workspace,
        issue_type=issue_type,
        severity=severity,
        title=title,
        description=description,
        suggested_action=suggested_action,
        affected_content_type=content_type,
        affected_object_id=object_id,
    )

    return 1


def _check_active_cakes_without_variants(workspace):
    count = 0

    for cake in Cake.objects.filter(is_active=True):
        if not CakeVariant.objects.filter(cake=cake).exists():
            count += _create_issue(
                workspace=workspace,
                issue_type=DataQualityIssue.ISSUE_ACTIVE_CAKE_WITHOUT_VARIANT,
                severity=DataQualityIssue.SEVERITY_WARNING,
                title=f"Active cake has no variant: {cake.name}",
                description="This active cake cannot be costed properly without a sellable variant.",
                suggested_action="Create at least one CakeVariant for this cake.",
                affected_object=cake,
            )

    return count


def _check_variants_without_recipes(workspace):
    count = 0

    for variant in CakeVariant.objects.filter(cake__is_active=True).select_related("cake"):
        has_recipe = Recipe.objects.filter(
            workspace=workspace,
            cake=variant.cake,
            variant=variant,
            is_active=True,
        ).exists()

        if not has_recipe:
            count += _create_issue(
                workspace=workspace,
                issue_type=DataQualityIssue.ISSUE_VARIANT_WITHOUT_RECIPE,
                severity=DataQualityIssue.SEVERITY_ERROR,
                title=f"Variant has no recipe: {variant}",
                description="A cake variant without a recipe cannot produce reliable ingredient cost.",
                suggested_action="Create a Recipe and RecipeLine records for this variant.",
                affected_object=variant,
            )

    return count


def _check_recipes_without_lines(workspace):
    count = 0

    for recipe in Recipe.objects.filter(workspace=workspace):
        if not recipe.lines.exists():
            count += _create_issue(
                workspace=workspace,
                issue_type=DataQualityIssue.ISSUE_RECIPE_WITHOUT_LINES,
                severity=DataQualityIssue.SEVERITY_ERROR,
                title=f"Recipe has no ingredient lines: {recipe.name}",
                description="A recipe without ingredient lines cannot be used for costing.",
                suggested_action="Add RecipeLine records for this recipe.",
                affected_object=recipe,
            )

    return count


def _check_paid_orders_without_items(workspace):
    count = 0

    paid_orders = BakeryOrder.objects.filter(
        workspace=workspace,
        status__in=[BakeryOrder.STATUS_PAID, BakeryOrder.STATUS_FULFILLED],
    )

    for order in paid_orders:
        if not order.items.exists():
            count += _create_issue(
                workspace=workspace,
                issue_type=DataQualityIssue.ISSUE_PAID_ORDER_WITHOUT_ITEMS,
                severity=DataQualityIssue.SEVERITY_CRITICAL,
                title=f"Paid order has no items: {order.order_number}",
                description="Paid orders without order items break revenue and product metrics.",
                suggested_action="Add order items or correct the order status.",
                affected_object=order,
            )

    return count


def _check_zero_total_orders(workspace):
    count = 0

    orders = BakeryOrder.objects.filter(
        workspace=workspace,
        status__in=[BakeryOrder.STATUS_PAID, BakeryOrder.STATUS_FULFILLED],
        total_amount__lte=Decimal("0.00"),
    )

    for order in orders:
        count += _create_issue(
            workspace=workspace,
            issue_type=DataQualityIssue.ISSUE_ZERO_TOTAL_ORDER,
            severity=DataQualityIssue.SEVERITY_ERROR,
            title=f"Paid order has zero total: {order.order_number}",
            description="A paid order with zero total will distort revenue and average order value.",
            suggested_action="Check pricing, discount, and payment status.",
            affected_object=order,
        )

    return count


def _check_low_stock_ingredients(workspace):
    count = 0

    for ingredient in Ingredient.objects.filter(workspace=workspace, is_active=True):
        if ingredient.current_stock_quantity <= ingredient.reorder_level_quantity:
            count += _create_issue(
                workspace=workspace,
                issue_type=DataQualityIssue.ISSUE_LOW_STOCK,
                severity=DataQualityIssue.SEVERITY_WARNING,
                title=f"Ingredient below reorder level: {ingredient.name}",
                description=(
                    f"Current stock is {ingredient.current_stock_quantity}; "
                    f"reorder level is {ingredient.reorder_level_quantity}."
                ),
                suggested_action="Review supplier lead time and reorder this ingredient.",
                affected_object=ingredient,
            )

    return count


def _check_near_expiry_lots(workspace, snapshot_date):
    count = 0
    expiry_limit = snapshot_date + timedelta(days=7)

    lots = IngredientLot.objects.filter(
        workspace=workspace,
        quantity_remaining__gt=Decimal("0.000"),
        expiry_date__isnull=False,
        expiry_date__lte=expiry_limit,
    ).select_related("ingredient")

    for lot in lots:
        count += _create_issue(
            workspace=workspace,
            issue_type=DataQualityIssue.ISSUE_NEAR_EXPIRY,
            severity=DataQualityIssue.SEVERITY_WARNING,
            title=f"Ingredient lot close to expiry: {lot.lot_code}",
            description=f"{lot.ingredient.name} expires on {lot.expiry_date}.",
            suggested_action="Use this lot in planned production or reduce future purchasing.",
            affected_object=lot,
        )

    return count


def _check_waste_without_reason(workspace):
    count = 0

    for waste_record in WasteRecord.objects.filter(workspace=workspace):
        if not waste_record.reason:
            count += _create_issue(
                workspace=workspace,
                issue_type=DataQualityIssue.ISSUE_WASTE_WITHOUT_REASON,
                severity=DataQualityIssue.SEVERITY_WARNING,
                title="Waste record without reason",
                description="Waste without a reason cannot support actionable analysis.",
                suggested_action="Classify the waste reason.",
                affected_object=waste_record,
            )

    return count


def _check_production_under_target(workspace):
    count = 0

    lines = ProductionBatchLine.objects.filter(
        batch__workspace=workspace,
        produced_quantity__lt=models_field_reference("planned_quantity"),
    )

    for line in lines:
        count += _create_issue(
            workspace=workspace,
            issue_type=DataQualityIssue.ISSUE_PRODUCTION_UNDER_DEMAND,
            severity=DataQualityIssue.SEVERITY_WARNING,
            title=f"Production under target: {line.recipe.name}",
            description=(
                f"Planned quantity was {line.planned_quantity}; "
                f"produced quantity was {line.produced_quantity}."
            ),
            suggested_action="Review failed quantity, production planning, and recipe execution.",
            affected_object=line,
        )

    return count


def _check_unallocated_production(workspace):
    count = 0

    lines = ProductionBatchLine.objects.filter(
        batch__workspace=workspace,
        produced_quantity__gt=Decimal("0.00"),
    )

    for line in lines:
        allocated_quantity = (
            line.allocations.aggregate(total=Sum("allocated_quantity"))["total"]
            or Decimal("0.00")
        )

        if line.produced_quantity > allocated_quantity:
            count += _create_issue(
                workspace=workspace,
                issue_type=DataQualityIssue.ISSUE_UNALLOCATED_PRODUCTION,
                severity=DataQualityIssue.SEVERITY_INFO,
                title=f"Production output not fully allocated: {line.recipe.name}",
                description=(
                    f"Produced quantity was {line.produced_quantity}; "
                    f"allocated quantity was {allocated_quantity}."
                ),
                suggested_action="Review whether remaining output was sold, stored, or wasted.",
                affected_object=line,
            )

    return count


def models_field_reference(field_name):
    from django.db.models import F

    return F(field_name)