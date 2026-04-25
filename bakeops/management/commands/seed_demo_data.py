from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed BakeOps demo data. Planned for a later V1 sprint."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING("seed_demo_data is planned but not implemented in Sprint 2.")
        )