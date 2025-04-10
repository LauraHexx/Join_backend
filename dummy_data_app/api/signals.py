from django.apps import AppConfig


class DummyDataAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dummy_data_app"  # Der Name deiner App

    def ready(self):
        import api.signals  # Importiere das Signal für diese App
