from decimal import Decimal, ROUND_HALF_UP


ZERO = Decimal("0.00")
MONEY_PLACES = Decimal("0.01")


def money(value):
    if value is None:
        return ZERO

    return Decimal(value).quantize(MONEY_PLACES, rounding=ROUND_HALF_UP)


def safe_percent(part, whole):
    part = Decimal(part or 0)
    whole = Decimal(whole or 0)

    if whole == 0:
        return ZERO

    return ((part / whole) * Decimal("100")).quantize(
        MONEY_PLACES,
        rounding=ROUND_HALF_UP,
    )


def get_recipe_for_order_item(order_item):
    from bakeops.models import Recipe

    recipe_qs = Recipe.objects.filter(
        cake=order_item.cake,
        is_active=True,
    ).select_related("cake", "variant")

    if order_item.variant_id:
        variant_recipe = recipe_qs.filter(variant=order_item.variant).first()

        if variant_recipe:
            return variant_recipe

    return recipe_qs.filter(variant__isnull=True).first() or recipe_qs.first()


def calculate_recipe_ingredient_unit_cost(recipe):
    if recipe is None:
        return ZERO

    total = ZERO

    for line in recipe.lines.select_related("ingredient").all():
        waste_multiplier = Decimal("1.00") + (
            Decimal(line.waste_factor_percent or 0) / Decimal("100")
        )
        line_cost = (
            Decimal(line.quantity_required or 0)
            * Decimal(line.ingredient.cost_per_unit or 0)
            * waste_multiplier
        )
        total += line_cost

    return money(total)


def calculate_order_item_ingredient_cost(order_item):
    recipe = get_recipe_for_order_item(order_item)

    if recipe is None:
        return ZERO

    unit_cost = calculate_recipe_ingredient_unit_cost(recipe)

    return money(unit_cost * Decimal(order_item.quantity or 0))


def calculate_order_ingredient_cost(order):
    total = ZERO

    for item in order.items.select_related("cake", "variant").all():
        total += calculate_order_item_ingredient_cost(item)

    return money(total)