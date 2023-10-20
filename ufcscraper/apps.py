from django.apps import AppConfig


class UfcscraperConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ufcscraper"

    # This is where you import your signals if you need any
    # def ready(self):
    #     import ufcscraper.signals
