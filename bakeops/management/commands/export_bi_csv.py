from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from bakeops.models import Workspace
from bakeops.services.exports import export_bi_csv


class Command(BaseCommand):
    help = "Export BakeOps BI-ready CSV files."

    def add_arguments(self, parser):
        parser.add_argument(
            "--workspace",
            type=str,
            default="SweetCakes Bakery",
            help="Workspace name to export. Defaults to SweetCakes Bakery.",
        )
        parser.add_argument(
            "--output-dir",
            type=str,
            default=None,
            help="Optional output directory. Defaults to the project exports/ folder.",
        )

    def handle(self, *args, **options):
        workspace_name = options["workspace"]
        output_dir = options["output_dir"]

        workspace = Workspace.objects.filter(name=workspace_name).first()

        if workspace is None:
            raise CommandError(
                f"Workspace not found: {workspace_name}. "
                "Run `python manage.py seed_demo_data --reset` first."
            )

        try:
            result = export_bi_csv(
                workspace=workspace,
                output_dir=Path(output_dir) if output_dir else None,
            )
        except Exception as exc:
            raise CommandError(f"CSV export failed: {exc}") from exc

        self.stdout.write(self.style.SUCCESS("BakeOps BI CSV exports generated successfully."))
        self.stdout.write(f"Workspace: {result['workspace']}")
        self.stdout.write(f"Output directory: {result['output_dir']}")
        self.stdout.write(f"Files generated: {result['file_count']}")
        self.stdout.write(f"Total rows exported: {result['row_count']}")

        for item in result["files"]:
            self.stdout.write(
                f"- {item['file']}: {item['rows']} rows, {item['columns']} columns"
            )