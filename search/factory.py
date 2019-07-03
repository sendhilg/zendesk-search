import factory

from .models import Organization, Ticket, User

factory.django.DjangoModelFactory


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    _id = factory.Sequence(lambda n: n)
    url = factory.Sequence(lambda n: 'http://initech.zendesk.com/api/v2/%s/organizations/1.json' % n)
    external_id = factory.Sequence(lambda n: '9270ed79-35eb-4a38-a46f-35725197ea8d%s' % n)
    name = factory.Sequence(lambda n: 'Enthaze%s' % n)
    domain_names = '["kage.com", "ecratic.com", "endipin.com", "zentix.com"]'
    created_at = '2016-05-21T11:10:28 -10:00'
    details = factory.Sequence(lambda n: 'MegaCorp%s' % n)
    shared_tickets = 'false'
    tags = '["Fulton", "West", "Rodriguez", "Farley"]'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    _id = factory.Sequence(lambda n: n)
    organization_id = factory.SubFactory(OrganizationFactory)
    url = factory.Sequence(lambda n: 'http://initech.zendesk.com/api/v2/%s/users/1.json' % n)
    external_id = factory.Sequence(lambda n: 'ce87e86c-4b45-483e-838f-ffbb5ffd5438%s' % n)
    name = factory.Sequence(lambda n: 'Deanna Terry%s' % n)
    alias = factory.Sequence(lambda n: 'Miss Lynda%s' % n)
    created_at = '2016-02-20T08:59:24 -11:00'
    active = 'false'
    verified = 'false'
    shared = 'false'
    locale = factory.Sequence(lambda n: 'jo%s' % n)
    timezone = factory.Sequence(lambda n: 'hn%s' % n)
    last_login_at = '2016-02-20T08:59:24 -11:00'
    email = factory.Sequence(lambda n: 'lyndaterry%s@flotonic.com' % n)
    phone = factory.Sequence(lambda n: '9924-522-038%s' % n)
    signature = factory.Sequence(lambda n: 'Dont Worry Be Happy!%s' % n)
    tags = factory.Sequence(lambda n: '["Toftrees", "Draper%s", "Northridge", "Cucumber"]' % n)
    suspended = 'false'
    role = 'admin'


class TicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ticket

    _id = factory.Sequence(lambda n: '436bf9b0%s' % n)
    url = factory.Sequence(lambda n: 'http://initech.zendesk.com/api/v2/tickets/436bf9b0%s.json' % n)
    external_id = factory.Sequence(lambda n: 'ce87e86c-4b45-483e-838f-ffbb5ffd5438%s' % n)
    created_at = '2016-02-20T08:59:24 -11:00'
    type = 'incident'
    subject = 'A Catastrophe in Korea (North)'
    description = 'Nostrud ad sit velit cupidatat laboris ipsum nisi amet laboris ex exercitation amet et proident.'
    priority = 'high'
    status = 'pending'
    submitter_id = factory.SubFactory(UserFactory)
    assignee_id = factory.SubFactory(UserFactory)
    organization_id = factory.SubFactory(OrganizationFactory)
    tags = '["Ohio", "Pennsylvania", "American Samoa", "Northern Mariana Islands"]'
    has_incidents = 'false'
    due_at = '2016-07-31T02:37:50 -10:00'
    via = 'web'
