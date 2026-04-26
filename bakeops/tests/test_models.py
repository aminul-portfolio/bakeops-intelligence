from django.test import TestCase

from bakeops.models import (
    BakeryOrder,
    Ingredient,
    ProductPerformanceSnapshot,
    Workspace,
)


class BakeOpsModelSmokeTests(TestCase):
    def test_workspace_string_representation(self):
        workspace = Workspace.objects.create(name="Test Bakery")

        self.assertEqual(str(workspace), "Test Bakery")

    def test_ingredient_string_representation(self):
        workspace = Workspace.objects.create(name="Test Bakery")
        ingredient = Ingredient.objects.create(
            workspace=workspace,
            name="Flour",
            unit=Ingredient.UNIT_KG,
            cost_per_unit="1.20",
            current_stock_quantity="10.000",
            reorder_level_quantity="5.000",
        )

        self.assertEqual(str(ingredient), "Flour")

    def test_product_performance_action_choices_include_review(self):
        actions = dict(ProductPerformanceSnapshot.ACTION_CHOICES)

        self.assertIn(ProductPerformanceSnapshot.ACTION_REVIEW, actions)

    def test_bakery_order_paid_status_exists(self):
        self.assertEqual(BakeryOrder.STATUS_PAID, "paid")