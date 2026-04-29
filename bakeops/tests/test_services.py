from django.core.management import call_command
from django.test import TestCase

from bakeops.models import (
    BakeryOrderItem,
    DataQualityIssue,
    ProductPerformanceSnapshot,
)
from bakeops.services.costing import calculate_order_item_ingredient_cost


class BakeOpsServiceTests(TestCase):
    def setUp(self):
        call_command("seed_demo_data", "--reset")
        call_command("build_bakery_metrics")

    def test_signature_product_revenue_rank_drops_after_waste(self):
        snapshot = ProductPerformanceSnapshot.objects.get(
            cake__name="Birthday Classic"
        )

        self.assertEqual(snapshot.revenue_rank, 1)
        self.assertEqual(snapshot.waste_adjusted_margin_rank, 4)
        self.assertEqual(snapshot.action_flag, ProductPerformanceSnapshot.ACTION_REVIEW)
        self.assertGreater(snapshot.waste_cost, 0)

    def test_promote_candidate_exists(self):
        snapshot = ProductPerformanceSnapshot.objects.get(
            cake__name="Lemon Poppy"
        )

        self.assertEqual(snapshot.action_flag, ProductPerformanceSnapshot.ACTION_PROMOTE)
        self.assertEqual(snapshot.waste_adjusted_margin_rank, 1)

    def test_data_quality_issues_are_generated(self):
        self.assertGreater(DataQualityIssue.objects.count(), 0)

    def test_order_item_ingredient_cost_is_positive(self):
        item = BakeryOrderItem.objects.select_related("cake", "variant").first()

        cost = calculate_order_item_ingredient_cost(item)

        self.assertGreater(cost, 0)