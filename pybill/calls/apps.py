from django.apps import AppConfig


class CallsConfig(AppConfig):
    name = 'pybill.calls'

    def ready(self):
        import pybill.calls.signals  # noqa
