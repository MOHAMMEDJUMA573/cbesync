from django.apps import AppConfig


class NtstaffsConfig(AppConfig):
    name = 'ntstaffs'
    def ready(self):
        import ntstaffs.signals