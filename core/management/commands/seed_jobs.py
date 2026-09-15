from django.core.management.base import BaseCommand
from django.core.management import call_command
from recruiters.models import Recruiter
from jobs.models import Job
from pathlib import Path


class Command(BaseCommand):
    help = "Load CampusHire recruiters and job data"

    def handle(self, *args, **options):

        # Create the recruiters required by jobs_data.json
        recruiters = [
            {
                "id": 1,
                "full_name": "Rahul Sharma",
                "email": "rahul@techsolutions.com",
                "phone": "9876543210",
                "company_name": "Tech Solutions",
                "company_description": "Tech Solutions is a software company providing innovative technology and web development solutions.",
                "company_website": "https://www.techsolutions.com",
                "company_location": "Bangalore",
            },
            {
                "id": 2,
                "full_name": "WebTech Recruiter",
                "email": "webtech@example.com",
                "phone": "9000000002",
                "company_name": "WebTech",
                "company_description": "WebTech is a technology company providing web development solutions.",
                "company_website": None,
                "company_location": "Hyderabad",
            },
            {
                "id": 3,
                "full_name": "DataWorks Recruiter",
                "email": "dataworks@example.com",
                "phone": "9000000003",
                "company_name": "DataWorks",
                "company_description": "DataWorks provides data analytics and technology solutions.",
                "company_website": None,
                "company_location": "Pune",
            },
            {
                "id": 4,
                "full_name": "Infosys Recruiter",
                "email": "infosys@example.com",
                "phone": "9000000004",
                "company_name": "Infosys",
                "company_description": "Infosys provides technology and digital transformation services.",
                "company_website": None,
                "company_location": "Bangalore",
            },
            {
                "id": 5,
                "full_name": "WebWorks Recruiter",
                "email": "webworks@example.com",
                "phone": "9000000005",
                "company_name": "WebWorks",
                "company_description": "WebWorks specializes in modern web development and frontend solutions.",
                "company_website": None,
                "company_location": "Chennai",
            },
            {
                "id": 6,
                "full_name": "TechNova Recruiter",
                "email": "technova@example.com",
                "phone": "9000000006",
                "company_name": "TechNova",
                "company_description": "TechNova develops innovative full-stack software solutions.",
                "company_website": None,
                "company_location": "Hyderabad",
            },
            {
                "id": 7,
                "full_name": "AI Labs Recruiter",
                "email": "ailabs@example.com",
                "phone": "9000000007",
                "company_name": "AI Labs",
                "company_description": "AI Labs develops artificial intelligence and machine learning solutions.",
                "company_website": None,
                "company_location": "Pune",
            },
            {
                "id": 8,
                "full_name": "FutureAI Recruiter",
                "email": "futureai@example.com",
                "phone": "9000000008",
                "company_name": "FutureAI",
                "company_description": "FutureAI develops innovative artificial intelligence solutions.",
                "company_website": None,
                "company_location": "Bangalore",
            },
            {
                "id": 9,
                "full_name": "SecureNet Recruiter",
                "email": "securenet@example.com",
                "phone": "9000000009",
                "company_name": "SecureNet",
                "company_description": "SecureNet is a technology company.",
                "company_website": None,
                "company_location": "Mumbai",
            },
            {
                "id": 10,
                "full_name": "CloudTech Recruiter",
                "email": "cloudtech@example.com",
                "phone": "9000000010",
                "company_name": "CloudTech",
                "company_description": "CloudTech is a technology company.",
                "company_website": None,
                "company_location": "Hyderabad",
            },
            {
                "id": 11,
                "full_name": "DevTech Recruiter",
                "email": "devtech@example.com",
                "phone": "9000000011",
                "company_name": "DevTech",
                "company_description": "DevTech is a technology company.",
                "company_website": None,
                "company_location": "Chennai",
            },
            {
                "id": 12,
                "full_name": "PythonWorks Recruiter",
                "email": "pythonworks@example.com",
                "phone": "9000000012",
                "company_name": "PythonWorks",
                "company_description": "PythonWorks is a technology company.",
                "company_website": None,
                "company_location": "Mysore",
            },
            {
                "id": 13,
                "full_name": "InnovateTech Recruiter",
                "email": "innovatetech@example.com",
                "phone": "9000000013",
                "company_name": "InnovateTech",
                "company_description": "InnovateTech is a technology company.",
                "company_website": None,
                "company_location": "Delhi",
            },
        ]

        self.stdout.write("Checking CampusHire recruiters...")

        for data in recruiters:
            recruiter_id = data["id"]

            Recruiter.objects.update_or_create(
                id=recruiter_id,
                defaults={
                    "full_name": data["full_name"],
                    "email": data["email"],
                    "phone": data["phone"],
                    "company_name": data["company_name"],
                    "company_description": data["company_description"],
                    "company_website": data["company_website"],
                    "company_location": data["company_location"],
                },
            )

        self.stdout.write(
            self.style.SUCCESS("CampusHire recruiters are ready.")
        )

        fixture = Path("jobs_data.json")

        if not fixture.exists():
            self.stdout.write(
                self.style.WARNING(
                    f"jobs_data.json not found at: {fixture.resolve()}"
                )
            )
            return

        # Do not reload the fixture if the jobs already exist.
        # This makes deployment/startup safe on Render.
        fixture_job_ids = [2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 17, 18, 19, 20]

        if Job.objects.filter(id__in=fixture_job_ids).exists():
            self.stdout.write(
                self.style.SUCCESS(
                    "CampusHire jobs already exist. Skipping fixture reload."
                )
            )
            return

        self.stdout.write(
            self.style.WARNING("Starting CampusHire job loading...")
        )

        try:
            call_command("loaddata", str(fixture))

            self.stdout.write(
                self.style.SUCCESS(
                    "CampusHire jobs loaded successfully."
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"ERROR loading CampusHire jobs: {e}"
                )
            )
            raise