from django.apps import AppConfig


class EmpConfig(AppConfig):
    name = 'emp'
    def ready(self):
        import emp.signals

