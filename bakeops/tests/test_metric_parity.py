import csv
from pathlib import Path
from tempfile import TemporaryDirectory

from django.core.management import call_command
from django.test import TestCase

from bakeops.models import DailyBakeryMetric, ProductPerformanceSnapshot
from bakeops.services.exports import export_bi_csv


class BakeOpsMetricParityTests(TestCase):
    def setUp(self):
        call_command("seed_demo_data", "--reset")
        call_command("build_bakery_metrics")

    def test_daily_metric_matches_daily_export(self):
        metric = DailyBakeryMetric.objects.first()

        with TemporaryDirectory() as temp_dir:
            export_bi_csv(output_dir=temp_dir)

            export_path = Path(temp_dir) / "daily_bakery_metrics.csv"

            with export_path.open(newline="", encoding="utf-8") as csv_file:
                rows = list(csv.DictReader(csv_file))

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["revenue"], str(metric.revenue))
        self.assertEqual(rows[0]["paid_orders"], str(metric.paid_orders))
        self.assertEqual(
            rows[0]["waste_adjusted_margin"],
            str(metric.waste_adjusted_margin),
        )

    def test_product_snapshot_export_preserves_signature_insight(self):
        birthday = ProductPerformanceSnapshot.objects.get(
            cake__name="Birthday Classic"
        )

        with TemporaryDirectory() as temp_dir:
            export_bi_csv(output_dir=temp_dir)

            export_path = Path(temp_dir) / "product_performance_snapshot.csv"

            with export_path.open(newline="", encoding="utf-8") as csv_file:
                rows = list(csv.DictReader(csv_file))

        birthday_row = next(
            row for row in rows if row["cake_name"] == "Birthday Classic"
        )

        self.assertEqual(birthday_row["revenue_rank"], str(birthday.revenue_rank))
        self.assertEqual(
            birthday_row["waste_adjusted_margin_rank"],
            str(birthday.waste_adjusted_margin_rank),
        )
        self.assertEqual(birthday_row["action_flag"], "review")