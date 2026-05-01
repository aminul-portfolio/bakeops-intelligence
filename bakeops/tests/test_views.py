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
        self.assertContains(response, "Revenue rank is not the same as margin strength.")
        self.assertContains(response, "Birthday Classic")
        self.assertContains(response, "ProductPerformanceSnapshot")
        self.assertContains(response, "margin-rank inversion")
        self.assertContains(response, "Deep-Dive Profitability Review")

    def test_product_profitability_route_is_correct(self):
        url = reverse("bakeops:product-profitability")
        match = resolve(url)

        self.assertEqual(url, "/analytics/products/")
        self.assertEqual(match.func, views.product_profitability)

    def test_ingredient_risk_view_builds_context(self):
        request = self.factory.get("/analytics/ingredients/")
        captured = {}

        def fake_render(request, template_name, context):
            captured["template_name"] = template_name
            captured["context"] = context

            return HttpResponse(
                "Ingredient Risk IngredientUsageSnapshot Butter Stock Position",
                status=200,
            )

        with patch("bakeops.views.render", side_effect=fake_render):
            response = views.ingredient_risk(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            captured["template_name"],
            "bakeops/ingredient_risk.html",
        )

        context = captured["context"]

        self.assertIsNotNone(context["latest_metric"])
        self.assertIsNotNone(context["workspace"])
        self.assertIsNotNone(context["snapshot_date"])
        self.assertEqual(context["ingredient_count"], 8)
        self.assertEqual(context["risk_count"], 5)
        self.assertGreater(len(context["ingredient_rows"]), 0)
        self.assertGreater(len(context["risk_rows"]), 0)

        top_risk_ingredient = context["top_risk_ingredient"]

        self.assertIsNotNone(top_risk_ingredient)
        self.assertEqual(top_risk_ingredient["ingredient"].name, "Butter")
        self.assertEqual(top_risk_ingredient["snapshot"].stock_risk_level, "high")
        self.assertTrue(top_risk_ingredient["is_stock_below_reorder"])
        self.assertEqual(top_risk_ingredient["current_stock"], top_risk_ingredient["snapshot"].current_stock_quantity)
        self.assertEqual(top_risk_ingredient["reorder_level"], top_risk_ingredient["snapshot"].reorder_level_quantity)

    @override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
    def test_ingredient_risk_page_loads(self):
        response = self.client.get(reverse("bakeops:ingredient-risk"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ingredient risk before production problems appear.")
        self.assertContains(response, "IngredientUsageSnapshot")
        self.assertContains(response, "Butter")
        self.assertContains(response, "high-risk ingredient rows")
        self.assertContains(response, "Stock Position")

    def test_ingredient_risk_route_is_correct(self):
        url = reverse("bakeops:ingredient-risk")
        match = resolve(url)

        self.assertEqual(url, "/analytics/ingredients/")
        self.assertEqual(match.func, views.ingredient_risk)

    def test_waste_analysis_view_builds_context(self):
        request = self.factory.get("/analytics/waste/")
        captured = {}

        def fake_render(request, template_name, context):
            captured["template_name"] = template_name
            captured["context"] = context

            return HttpResponse(
                "Waste Analysis WasteRecord Birthday Classic Product Waste Impact",
                status=200,
            )

        with patch("bakeops.views.render", side_effect=fake_render):
            response = views.waste_analysis(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            captured["template_name"],
            "bakeops/waste_analysis.html",
        )

        context = captured["context"]

        self.assertIsNotNone(context["latest_metric"])
        self.assertIsNotNone(context["workspace"])
        self.assertIsNotNone(context["snapshot_date"])
        self.assertEqual(context["total_waste_records"], 4)
        self.assertGreater(context["total_waste_cost"], 0)
        self.assertGreater(context["gross_margin"], 0)
        self.assertGreater(context["waste_adjusted_margin"], 0)
        self.assertGreater(len(context["waste_records"]), 0)
        self.assertGreater(len(context["product_waste_rows"]), 0)
        self.assertGreater(len(context["waste_reason_rows"]), 0)

        top_waste_product = context["top_waste_product"]

        self.assertIsNotNone(top_waste_product)
        self.assertEqual(top_waste_product["cake"].name, "Birthday Classic")
        self.assertGreater(top_waste_product["waste_cost"], 0)
        self.assertEqual(top_waste_product["action_flag"], "review")

    @override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
    def test_waste_analysis_page_loads(self):
        response = self.client.get(reverse("bakeops:waste-analysis"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Waste explains why revenue alone is not enough.")
        self.assertContains(response, "WasteRecord")
        self.assertContains(response, "Birthday Classic")
        self.assertContains(response, "Waste-adjusted Margin")
        self.assertContains(response, "Product Waste Impact")

    def test_waste_analysis_route_is_correct(self):
        url = reverse("bakeops:waste-analysis")
        match = resolve(url)

        self.assertEqual(url, "/analytics/waste/")
        self.assertEqual(match.func, views.waste_analysis)

    def test_occasion_analytics_view_builds_context(self):
        request = self.factory.get("/analytics/occasions/")
        captured = {}

        def fake_render(request, template_name, context):
            captured["template_name"] = template_name
            captured["context"] = context

            return HttpResponse(
                "Occasion Analytics OccasionDemandSnapshot Birthday",
                status=200,
            )

        with patch("bakeops.views.render", side_effect=fake_render):
            response = views.occasion_analytics(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            captured["template_name"],
            "bakeops/occasion_analytics.html",
        )

        context = captured["context"]

        self.assertIsNotNone(context["latest_metric"])
        self.assertIsNotNone(context["workspace"])
        self.assertIsNotNone(context["snapshot_date"])
        self.assertEqual(context["occasion_count"], 4)
        self.assertEqual(context["total_occasion_orders"], 6)
        self.assertEqual(context["total_quantity_sold"], 15)
        self.assertEqual(context["total_upcoming_orders"], 6)
        self.assertEqual(context["total_delivery_pressure"], 3)
        self.assertGreater(context["total_occasion_revenue"], 0)
        self.assertGreater(len(context["occasion_rows"]), 0)

        top_occasion = context["top_occasion"]

        self.assertIsNotNone(top_occasion)
        self.assertEqual(top_occasion["occasion"].name, "Birthday")
        self.assertEqual(top_occasion["snapshot"].order_count, 3)
        self.assertEqual(top_occasion["snapshot"].quantity_sold, 9)

    @override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
    def test_occasion_analytics_page_loads(self):
        response = self.client.get(reverse("bakeops:occasion-analytics"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Occasion demand shows where bakery planning pressure comes from.",
        )
        self.assertContains(response, "OccasionDemandSnapshot")
        self.assertContains(response, "Birthday")
        self.assertContains(response, "Occasion Demand Deep Dive")
        self.assertContains(response, "Delivery Pressure")

    def test_occasion_analytics_route_is_correct(self):
        url = reverse("bakeops:occasion-analytics")
        match = resolve(url)

        self.assertEqual(url, "/analytics/occasions/")
        self.assertEqual(match.func, views.occasion_analytics)

    def test_customer_analytics_view_builds_context(self):
        request = self.factory.get("/analytics/customers/")
        captured = {}

        def fake_render(request, template_name, context):
            captured["template_name"] = template_name
            captured["context"] = context

            return HttpResponse(
                "Customer Analytics CustomerLoyaltySnapshot Maya Patel",
                status=200,
            )

        with patch("bakeops.views.render", side_effect=fake_render):
            response = views.customer_analytics(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            captured["template_name"],
            "bakeops/customer_analytics.html",
        )

        context = captured["context"]

        self.assertIsNotNone(context["latest_metric"])
        self.assertIsNotNone(context["workspace"])
        self.assertIsNotNone(context["snapshot_date"])
        self.assertEqual(context["customer_count"], 5)
        self.assertEqual(context["repeat_customer_count"], 3)
        self.assertEqual(context["new_customer_count"], 2)
        self.assertEqual(context["total_customer_orders"], 6)
        self.assertEqual(context["total_loyalty_points_earned"], 32)
        self.assertEqual(context["total_current_points_balance"], 475)
        self.assertGreater(context["total_customer_revenue"], 0)
        self.assertGreater(len(context["customer_rows"]), 0)

        top_customer = context["top_customer"]

        self.assertIsNotNone(top_customer)
        self.assertEqual(top_customer["customer"].full_name, "Maya Patel")
        self.assertEqual(top_customer["snapshot"].total_orders, 2)
        self.assertTrue(top_customer["snapshot"].is_repeat_customer)

    @override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
    def test_customer_analytics_page_loads(self):
        response = self.client.get(reverse("bakeops:customer-analytics"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Customer loyalty shows where bakery revenue is concentrated.",
        )
        self.assertContains(response, "CustomerLoyaltySnapshot")
        self.assertContains(response, "Maya Patel")
        self.assertContains(response, "Customer Loyalty Deep Dive")
        self.assertContains(response, "Repeat Customers")

    def test_customer_analytics_route_is_correct(self):
        url = reverse("bakeops:customer-analytics")
        match = resolve(url)

        self.assertEqual(url, "/analytics/customers/")
        self.assertEqual(match.func, views.customer_analytics)

    def test_data_quality_review_view_builds_context(self):
        request = self.factory.get("/analytics/data-quality/")
        captured = {}

        def fake_render(request, template_name, context):
            captured["template_name"] = template_name
            captured["context"] = context

            return HttpResponse(
                "Data Quality Review DataQualityIssue Ingredient below reorder level: Butter",
                status=200,
            )

        with patch("bakeops.views.render", side_effect=fake_render):
            response = views.data_quality_review(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            captured["template_name"],
            "bakeops/data_quality_review.html",
        )

        context = captured["context"]

        self.assertIsNotNone(context["latest_metric"])
        self.assertIsNotNone(context["workspace"])
        self.assertIsNotNone(context["snapshot_date"])
        self.assertEqual(context["total_issue_count"], 12)
        self.assertEqual(context["open_issue_count"], 12)
        self.assertEqual(context["warning_issue_count"], 11)
        self.assertEqual(context["info_issue_count"], 1)
        self.assertGreaterEqual(context["high_priority_issue_count"], 1)
        self.assertGreater(len(context["issue_rows"]), 0)
        self.assertGreater(len(context["open_issue_rows"]), 0)
        self.assertGreater(len(context["severity_summary"]), 0)
        self.assertGreater(len(context["issue_type_summary"]), 0)
        self.assertGreater(len(context["status_summary"]), 0)

        top_issue = context["top_issue"]

        self.assertIsNotNone(top_issue)
        self.assertEqual(top_issue["issue"].status, "open")
        self.assertEqual(top_issue["severity_label"], "Warning")
        self.assertTrue(top_issue["is_high_priority"])

    @override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
    def test_data_quality_review_page_loads(self):
        response = self.client.get(reverse("bakeops:data-quality-review"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Trust the analytics layer by making quality issues visible.",
        )
        self.assertContains(response, "DataQualityIssue")
        self.assertContains(response, "Ingredient below reorder level: Butter")
        self.assertContains(response, "Data Quality Issue Register")
        self.assertContains(response, "Trust Evidence")

    def test_data_quality_review_route_is_correct(self):
        url = reverse("bakeops:data-quality-review")
        match = resolve(url)

        self.assertEqual(url, "/analytics/data-quality/")
        self.assertEqual(match.func, views.data_quality_review)

    def test_export_centre_view_builds_context(self):
        request = self.factory.get("/analytics/exports/")
        captured = {}

        def fake_render(request, template_name, context):
            captured["template_name"] = template_name
            captured["context"] = context

            return HttpResponse(
                "Export Centre BI-ready exports with a visible contract.",
                status=200,
            )

        with patch("bakeops.views.render", side_effect=fake_render):
            response = views.export_centre(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            captured["template_name"],
            "bakeops/export_centre.html",
        )

        context = captured["context"]

        self.assertIsNotNone(context["latest_metric"])
        self.assertIsNotNone(context["workspace"])
        self.assertIsNotNone(context["snapshot_date"])
        self.assertEqual(context["export_count"], 11)
        self.assertEqual(context["fact_export_count"], 4)
        self.assertEqual(context["dimension_export_count"], 5)
        self.assertEqual(context["gold_export_count"], 2)
        self.assertEqual(context["export_command"], "python manage.py export_bi_csv")
        self.assertEqual(context["output_folder"], "exports/")
        self.assertGreater(len(context["export_cards"]), 0)
        self.assertGreater(len(context["contract_principles"]), 0)

        file_names = {
            card["file_name"]
            for card in context["export_cards"]
        }

        self.assertIn("fact_orders.csv", file_names)
        self.assertIn("product_performance_snapshot.csv", file_names)

    @override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
    def test_export_centre_page_loads(self):
        response = self.client.get(reverse("bakeops:export-centre"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BI-ready exports with a visible contract.")
        self.assertContains(response, "python manage.py export_bi_csv")
        self.assertContains(response, "fact_orders.csv")
        self.assertContains(response, "product_performance_snapshot.csv")

    def test_export_centre_route_is_correct(self):
        url = reverse("bakeops:export-centre")
        match = resolve(url)

        self.assertEqual(url, "/analytics/exports/")
        self.assertEqual(match.func, views.export_centre)