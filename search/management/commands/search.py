from django.core.management.base import BaseCommand

from search.controller import AppController


class Command(BaseCommand):
    help = 'Search zendesk'

    def handle(self, *args, **kwargs):
        app_controller = AppController()
        app_controller.run()
