from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from bakeops.models import (
    BakeryMetricRunLog,
    BakeryOrder,
    DailyBakeryMetric,
    ProductPerformanceSnapshot,
    WasteRecord,
    Workspace,
)


class BakeOpsCommandTests(TestCase):
    def test_seed_demo_data_command_creates_demo_dataset(self):
        out = StringIO()

        call_command("seed_demo_data", "--reset", stdout=out)

        self.assertIn("BakeOps demo data seeded successfully", out.getvalue())
        self.assertEqual(Workspace.objects.filter(name="SweetCakes Bakery").count(), 1)
        self.assertEqual(BakeryOrder.objects.count(), 7)
        self.assertEqual(WasteRecord.objects.count(), 4)

    def test_build_bakery_metrics_command_creates_gold_layer_records(self):
        call_command("seed_demo_data", "--reset")

        out = StringIO()
        call_command("build_bakery_metrics", stdout=out)

        self.assertIn("BakeOps bakery metrics built successfully", out.getvalue())
        self.assertEqual(DailyBakeryMetric.objects.count(), 1)
        self.assertEqual(ProductPerformanceSnapshot.objects.count(), 4)
        self.assertEqual(BakeryMetricRunLog.objects.filter(status="success").count(), 1)

    def test_export_bi_csv_command_runs_after_metric_build(self):
        call_command("seed_demo_data", "--reset")
        call_command("build_bakery_metrics")

        out = StringIO()
        call_command("export_bi_csv", stdout=out)

        output = out.getvalue()

        self.assertIn("BakeOps BI CSV exports generated successfully", output)
        self.assertIn("Files generated: 11", output)