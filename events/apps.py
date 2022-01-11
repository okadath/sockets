from django.apps import AppConfig


class EventsConfig(AppConfig):
    name = 'events'
    def ready(self):
        # señal para la creacion del profile automaticamente 
        # al crear un usuario, remove?
        import events.signals