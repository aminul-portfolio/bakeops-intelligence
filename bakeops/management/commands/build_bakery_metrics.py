from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Build BakeOps bakery metrics. Planned for a later V1 sprint."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING("build_bakery_metrics is planned but not implemented in Sprint 2.")
        )