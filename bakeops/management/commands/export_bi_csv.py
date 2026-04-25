from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Export BakeOps BI-ready CSV files. Planned for a later V1 sprint."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING("export_bi_csv is planned but not implemented in Sprint 2.")
        )