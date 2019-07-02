import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from search.models import Organization, Ticket, User


class Command(BaseCommand):
    help = 'Load Data'

    def handle(self, *args, **kwargs):
        load_data = LoadData()
        load_data.run()


class LoadData(object):
    def run(self):
        Ticket.objects.all().delete()
        User.objects.all().delete()
        Organization.objects.all().delete()
        
        with open('organizations.json', encoding='utf-8') as data_file:
            json_data = json.loads(data_file.read())
            Organization.objects.bulk_create(
                [Organization(**row) for row in json_data]
            )

        with open('users.json', encoding='utf-8') as data_file:
            json_data = json.loads(data_file.read())
            for user_data in json_data:
                try:
                    organization_id = Organization.objects.get(_id=user_data.get('organization_id'))
                except ObjectDoesNotExist:
                    organization_id = None
                user_data['organization_id'] = organization_id
                user = User(**user_data)
                user.save()

        with open('tickets.json', encoding='utf-8') as data_file:
            json_data = json.loads(data_file.read())
            for ticket_data in json_data:
                try:
                    organization_id = Organization.objects.get(_id=ticket_data.get('organization_id'))
                except ObjectDoesNotExist:
                    organization_id = None
                try:
                    submitter_id = User.objects.get(_id=ticket_data.get('submitter_id'))
                except ObjectDoesNotExist:
                    submitter_id = None
                try:
                    assignee_id = User.objects.get(_id=ticket_data.get('assignee_id'))
                except ObjectDoesNotExist:
                    assignee_id = None
                ticket_data['organization_id'] = organization_id
                ticket_data['submitter_id'] = submitter_id
                ticket_data['assignee_id'] = assignee_id
                ticket = Ticket(**ticket_data)
                ticket.save()
