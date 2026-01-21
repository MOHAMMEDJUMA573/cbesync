from django.apps import AppConfig


class TeachersConfig(AppConfig):
    name = 'teachers'

    def ready(self):
        import teachers.signals