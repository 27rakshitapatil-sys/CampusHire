from django.core.management.base import BaseCommand
from django.core.management import call_command
from pathlib import Path


class Command(BaseCommand):
    help = "Load CampusHire job data"

    def handle(self, *args, **options):
        fixture = Path("jobs_data.json")

        if not fixture.exists():
            self.stdout.write(
                self.style.WARNING("jobs_data.json not found.")
            )
            return

        call_command("loaddata", str(fixture))
        self.stdout.write(
            self.style.SUCCESS("CampusHire jobs loaded successfully.")
        )
