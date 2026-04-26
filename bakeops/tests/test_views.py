from unittest.mock import patch

from django.core.management import call_command
from django.http import HttpResponse
from django.test import RequestFactory, TestCase, override_settings
from django.urls import resolve, reverse

from bakeops import views


class BakeOpsDashboardViewTests(TestCase):
    def setUp(self):
        call_command("seed_demo_data", "--reset")
        call_command("build_bakery_metrics")
        self.factory = RequestFactory()

    def test_analytics_dashboard_view_builds_context(self):
        request = self.factory.get("/analytics/")
        captured = {}

        def fake_render(request, template_name, context):
            captured["template_name"] = template_name
            captured["context"] = context

            return HttpResponse(
                "BakeOps Intelligence Waste-adjusted profitability "
                "Birthday Classic Product Profitability",
                status=200,
            )

        with patch("bakeops.views.render", side_effect=fake_render):
            response = views.analytics_dashboard(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            captured["template_name"],
            "bakeops/analytics_dashboard.html",
        )

        context = captured["context"]

        self.assertIsNotNone(context["latest_metric"])
        self.assertIsNotNone(context["workspace"])
        self.assertIsNotNone(context["snapshot_date"])
        self.assertGreater(len(context["product_snapshots"]), 0)
        self.assertGreater(len(context["weekly_actions"]), 0)

        signature_product = context["signature_product"]

        self.assertIsNotNone(signature_product)
        self.assertEqual(signature_product.cake.name, "Birthday Classic")
        self.assertEqual(signature_product.revenue_rank, 1)
        self.assertEqual(signature_product.waste_adjusted_margin_rank, 4)

    def test_analytics_dashboard_route_is_correct(self):
        url = reverse("bakeops:analytics-dashboard")
        match = resolve(url)

        self.assertEqual(url, "/analytics/")
        self.assertEqual(match.func, views.analytics_dashboard)

    def test_product_profitability_view_builds_context(self):
        request = self.factory.get("/analytics/products/")
        captured = {}

        def fake_render(request, template_name, context):
            captured["template_name"] = template_name
            captured["context"] = context

            return HttpResponse(
                "Product Profitability Birthday Classic margin-rank inversion",
                status=200,
            )

        with patch("bakeops.views.render", side_effect=fake_render):
            response = views.product_profitability(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            captured["template_name"],
            "bakeops/product_profitability.html",
        )

        context = captured["context"]

        self.assertIsNotNone(context["latest_metric"])
        self.assertIsNotNone(context["workspace"])
        self.assertIsNotNone(context["snapshot_date"])
        self.assertGreater(context["product_count"], 0)
        self.assertGreater(len(context["product_rows"]), 0)
        self.assertGreaterEqual(context["review_count"], 1)
        self.assertGreaterEqual(context["inversion_count"], 1)

        signature_product = context["signature_product"]

        self.assertIsNotNone(signature_product)
        self.assertEqual(signature_product.cake.name, "Birthday Classic")
        self.assertEqual(signature_product.revenue_rank, 1)
        self.assertEqual(signature_product.waste_adjusted_margin_rank, 4)
        self.assertEqual(signature_product.action_flag, "review")

        birthday_row = next(
            row
            for row in context["product_rows"]
            if row["product"].cake.name == "Birthday Classic"
        )

        self.assertEqual(birthday_row["revenue_rank"], 1)
        self.assertEqual(birthday_row["waste_adjusted_margin_rank"], 4)
        self.assertEqual(birthday_row["margin_rank_gap"], 3)
        self.assertTrue(birthday_row["has_margin_rank_inversion"])
        self.assertEqual(birthday_row["flag_label"], "Review")
        self.assertTrue(birthday_row["is_signature"])

    @override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
    def test_product_profitability_page_loads(self):
        response = self.client.get(reverse("bakeops:product-profitability"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Product profitability beyond revenue ranking.")
        self.assertContains(response, "Birthday Classic")
        self.assertContains(response, "ProductPerformanceSnapshot")
        self.assertContains(response, "margin-rank inversion")

    def test_product_profitability_route_is_correct(self):
        url = reverse("bakeops:product-profitability")
        match = resolve(url)

        self.assertEqual(url, "/analytics/products/")
        self.assertEqual(match.func, views.product_profitability)