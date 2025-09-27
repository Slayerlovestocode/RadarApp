# reports/management/commands/seed_data.py

import random
from datetime import datetime, timedelta
import pytz

from django.core.management.base import BaseCommand
from reports.models import Report

class Command(BaseCommand):
    help = 'Seeds the database with dummy report data for Switzerland.'

    def handle(self, *args, **kwargs):
        # Optional: Clear existing reports to avoid duplicates on re-runs
        self.stdout.write('Deleting existing reports...')
        Report.objects.all().delete()

        locations = [
            "Geneva, Switzerland",
            "Zurich, Switzerland",
            "Bern, Switzerland",
            "Lausanne, Switzerland",
            "Lucerne, Switzerland",
            "Basel, Switzerland",
            "St. Gallen, Switzerland",
            "Lugano, Switzerland",
            "Winterthur, Switzerland",
            "Interlaken, Switzerland",
            "Zermatt, Switzerland",
            "Montreux, Switzerland",
            "Chur, Switzerland",
            "Fribourg, Switzerland",
            "Thun, Switzerland"
        ]

        incident_types = [choice[0] for choice in Report.INCIDENT_TYPE_CHOICES]
        
        self.stdout.write('Creating new dummy reports...')
        for location in locations:
            # Create a few reports per location to create "hotspots"
            for _ in range(random.randint(1, 4)):
                report = Report.objects.create(
                    incident_type=random.choice(incident_types),
                    incident_datetime=datetime.now(pytz.UTC) - timedelta(days=random.randint(1, 365)),
                    location=location,
                    description=f"This is a dummy report for an incident in {location.split(',')[0]}.",
                )
                # Re-fetch the report from the database to get the updated values from the save() method
                report.refresh_from_db()

                # Verify that geocoding was successful
                if report.latitude and report.longitude:
                    self.stdout.write(self.style.SUCCESS(f'Successfully created and geocoded report for: {location}'))
                else:
                    self.stdout.write(self.style.ERROR(f'CRITICAL: Failed to geocode report for location: {location}. The geocoding service may be down or rate-limiting requests.'))


        self.stdout.write(self.style.SUCCESS('Database has been seeded with dummy data!'))