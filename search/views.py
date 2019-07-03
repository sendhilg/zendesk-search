from django.core.exceptions import FieldError

from .models import Organization, Ticket, User


class InvalidSearchTermException(Exception):
    pass


class Search(object):

    def __init__(self, search_term, search_value):
        self.search_term = search_term
        self.search_value = search_value

    def search_organizations(self):
        kwargs = {
            '{0}__{1}'.format(self.search_term, 'icontains'): self.search_value,
        }

        try:
            qs = Organization.objects.filter(**kwargs).prefetch_related('users', 'tickets')
        except FieldError:
            raise InvalidSearchTermException(
                f'Invalid search term "{self.search_term}" for organizations search.'
            )
        return qs

    def search_users(self):
        self.model_search_term = self.search_term

        if self.search_term == 'organization_id':
            self.model_search_term = 'organization_id___id'

        kwargs = {
            '{0}__{1}'.format(self.model_search_term, 'icontains'): self.search_value,
        }

        try:
            qs = User.objects.filter(
                    **kwargs,
                ).select_related(
                    'organization_id',
                ).prefetch_related(
                    'submitted_tickets',
                    'assigned_tickets',
                )
        except FieldError:
            raise InvalidSearchTermException(
                f'Invalid search term "{self.search_term}" for users search.'
            )
        return qs

    def search_tickets(self):
        self.model_search_term = self.search_term

        if self.search_term == 'organization_id':
            self.model_search_term = 'organization_id___id'
        if self.search_term == 'submitter_id':
            self.model_search_term = 'submitter_id___id'
        if self.search_term == 'assignee_id':
            self.model_search_term = 'assignee_id___id'

        kwargs = {
            '{0}__{1}'.format(self.model_search_term, 'icontains'): self.search_value,
        }

        try:
            qs = Ticket.objects.filter(
                **kwargs
            ).select_related('organization_id', 'submitter_id', 'assignee_id')
        except FieldError:
            raise InvalidSearchTermException(
                f'Invalid search term "{self.search_term}" for tickets search.'
            )
        return qs
