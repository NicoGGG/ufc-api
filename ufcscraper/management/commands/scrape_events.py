from django.core.management.base import BaseCommand
from ufcscraper.tasks import scrape_all_ufc_events


class Command(BaseCommand):
    help = "Scrape last n UFC event"

    def add_arguments(self, parser):
        parser.add_argument("last", type=int, help="Last n event scrape", default=1)

    def handle(self, *args, **kwargs):
        last = kwargs["last"]
        scrape_all_ufc_events(last).apply_async()
        self.stdout.write(
            self.style.SUCCESS(
                "Successfully triggered task to scrape upcoming UFC event"
            )
        )
