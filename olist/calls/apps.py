from django.apps import AppConfig


class CallsConfig(AppConfig):
    name = 'olist.calls'

    def ready(self):
        import olist.calls.signals  # noqa
