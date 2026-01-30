from django.apps import AppConfig



class ParentsConfig(AppConfig):
    name = 'parents'
    def ready(self):
        import parents.signals
