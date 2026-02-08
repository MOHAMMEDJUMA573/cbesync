from django.apps import AppConfig


class SubjectsConfig(AppConfig):
    name = 'subjects'

    def ready(self):
        import subjects.signals