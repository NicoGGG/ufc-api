from django.core.management.base import BaseCommand
from ufcscraper.tasks import scrape_all_ufc_fighters


class Command(BaseCommand):
    help = "Scrape all UFC fighters"

    def handle(self, *args, **kwargs):
        scrape_all_ufc_fighters.apply_async()
        self.stdout.write(
            self.style.SUCCESS("Successfully triggered task to scrape all UFC fighters")
        )
