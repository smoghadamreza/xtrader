import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to wait for the database"""

    def handle(self, *args, **options):
        self.stdout.write("Waiting for the database...")

        db_up = False
        while not db_up:
            try:
                # Check all the database connections
                for db_name in connections:
                    self.check(databases=[db_name])

                db_up = True
            except OperationalError:
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database is ready!"))
