from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from bakeops.models import BakeryMetricRunLog, Workspace
from bakeops.services.analytics import build_bakery_metrics


class Command(BaseCommand):
    help = "Build BakeOps gold-layer bakery metrics from operational data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--workspace",
            type=str,
            default="SweetCakes Bakery",
            help="Workspace name to build metrics for. Defaults to SweetCakes Bakery.",
        )
        parser.add_argument(
            "--date",
            type=str,
            default=None,
            help="Snapshot date in YYYY-MM-DD format. Defaults to today.",
        )

    def handle(self, *args, **options):
        workspace_name = options["workspace"]
        snapshot_date = self._parse_snapshot_date(options["date"])

        workspace = Workspace.objects.filter(name=workspace_name).first()

        if workspace is None:
            raise CommandError(
                f"Workspace not found: {workspace_name}. "
                "Run `python manage.py seed_demo_data --reset` first."
            )

        run_log = BakeryMetricRunLog.objects.create(
            workspace=workspace,
            command_name="build_bakery_metrics",
            status=BakeryMetricRunLog.STATUS_STARTED,
            started_at=timezone.now(),
            notes=f"Building metrics for snapshot date {snapshot_date}.",
        )

        try:
            summary = build_bakery_metrics(
                workspace=workspace,
                snapshot_date=snapshot_date,
            )
        except Exception as exc:
            finished_at = timezone.now()

            run_log.status = BakeryMetricRunLog.STATUS_FAILED
            run_log.finished_at = finished_at
            run_log.duration_seconds = Decimal(
                str(round((finished_at - run_log.started_at).total_seconds(), 3))
            )
            run_log.error_message = str(exc)
            run_log.save()

            raise CommandError(f"Metric build failed: {exc}") from exc

        finished_at = timezone.now()

        run_log.status = BakeryMetricRunLog.STATUS_SUCCESS
        run_log.finished_at = finished_at
        run_log.duration_seconds = Decimal(
            str(round((finished_at - run_log.started_at).total_seconds(), 3))
        )
        run_log.rows_processed = summary["rows_processed"]
        run_log.metrics_created = summary["metrics_created"]
        run_log.snapshots_created = summary["snapshots_created"]
        run_log.issues_created = summary["issues_created"]
        run_log.notes = (
            f"Processed {summary['workspaces_processed']} workspace(s) "
            f"for snapshot date {snapshot_date}."
        )
        run_log.save()

        self.stdout.write(self.style.SUCCESS("BakeOps bakery metrics built successfully."))
        self.stdout.write(f"Workspace: {workspace.name}")
        self.stdout.write(f"Snapshot date: {snapshot_date}")
        self.stdout.write(f"Rows processed: {summary['rows_processed']}")
        self.stdout.write(f"Metrics created: {summary['metrics_created']}")
        self.stdout.write(f"Snapshots created: {summary['snapshots_created']}")
        self.stdout.write(f"Issues created: {summary['issues_created']}")

    def _parse_snapshot_date(self, value):
        if not value:
            return date.today()

        try:
            return date.fromisoformat(value)
        except ValueError as exc:
            raise CommandError("Invalid --date. Use YYYY-MM-DD format.") from exc