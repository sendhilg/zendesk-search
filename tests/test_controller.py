import pytest

from search.controller import AppController
from search.factory import OrganizationFactory, TicketFactory, UserFactory
from search.views import Search


@pytest.mark.django_db
def test_search_organizations(capsys):
    organization = OrganizationFactory()
    UserFactory(organization_id=organization)
    TicketFactory(organization_id=organization)

    controller = AppController()
    controller.search_term = '_id'
    controller.search_value = organization._id
    controller.search = Search(controller.search_term, controller.search_value)
    controller.search_organizations()

    captured = capsys.readouterr()

    assert (
        f'Searching organizations for {controller.search_term} with a value of {controller.search_value}'
    ) in captured.out

    assert '_id' in captured.out
    assert 'url' in captured.out
    assert 'name' in captured.out
    assert 'domain_names' in captured.out
    assert 'created_at' in captured.out
    assert 'details' in captured.out
    assert 'shared_tickets' in captured.out
    assert 'tags' in captured.out
    assert 'user_id' in captured.out
    assert 'user_name' in captured.out
    assert 'ticket_id' in captured.out
    assert 'ticket_subject' in captured.out


@pytest.mark.django_db
def test_search_organizations_for_no_data(capsys):
    controller = AppController()
    controller.search_term = '_id'
    controller.search_value = 1
    controller.search = Search(controller.search_term, controller.search_value)
    controller.search_organizations()

    captured = capsys.readouterr()

    assert (
        f'No results found for search term {controller.search_term} '
        f'and search value {controller.search_value}'
    ) in captured.out


@pytest.mark.django_db
def test_search_organizations_for_invalid_search_term(capsys):
    controller = AppController()
    controller.search_term = 'unknown'
    controller.search_value = 1
    controller.search = Search(controller.search_term, controller.search_value)
    controller.search_organizations()

    captured = capsys.readouterr()

    assert f'Invalid search term "{controller.search_term}"' in captured.out


@pytest.mark.django_db
def test_search_users(capsys):
    user = UserFactory()
    TicketFactory(assignee_id=user)
    TicketFactory(submitter_id=user)

    controller = AppController()
    controller.search_term = '_id'
    controller.search_value = user._id
    controller.search = Search(controller.search_term, controller.search_value)
    controller.search_users()

    captured = capsys.readouterr()

    assert (
        f'Searching users for {controller.search_term} with a value of {controller.search_value}'
    ) in captured.out

    assert '_id' in captured.out
    assert 'url' in captured.out
    assert 'external_id' in captured.out
    assert 'name' in captured.out
    assert 'alias' in captured.out
    assert 'created_at' in captured.out
    assert 'active' in captured.out
    assert 'verified' in captured.out
    assert 'shared' in captured.out
    assert 'locale' in captured.out
    assert 'timezone' in captured.out
    assert 'last_login_at' in captured.out
    assert 'email' in captured.out
    assert 'phone' in captured.out
    assert 'signature' in captured.out
    assert 'organization_id' in captured.out
    assert 'orgnaization_name' in captured.out
    assert 'tags' in captured.out
    assert 'suspended' in captured.out
    assert 'role' in captured.out
    assert 'submitted_ticket_id' in captured.out
    assert 'submitted_ticket_subject' in captured.out
    assert 'assigned_ticket_id' in captured.out
    assert 'assigned_ticket_subject' in captured.out


@pytest.mark.django_db
def test_search_users_for_no_data(capsys):
    controller = AppController()
    controller.search_term = '_id'
    controller.search_value = 1
    controller.search = Search(controller.search_term, controller.search_value)
    controller.search_users()

    captured = capsys.readouterr()

    assert (
        f'No results found for search term {controller.search_term} '
        f'and search value {controller.search_value}'
    ) in captured.out


@pytest.mark.django_db
def test_search_users_for_invalid_search_term(capsys):
    controller = AppController()
    controller.search_term = 'unknown'
    controller.search_value = 1
    controller.search = Search(controller.search_term, controller.search_value)
    controller.search_organizations()

    captured = capsys.readouterr()

    assert f'Invalid search term "{controller.search_term}"' in captured.out


@pytest.mark.django_db
def test_search_tickets(capsys):
    ticket = TicketFactory()

    controller = AppController()
    controller.search_term = '_id'
    controller.search_value = ticket._id
    controller.search = Search(controller.search_term, controller.search_value)
    controller.search_tickets()

    captured = capsys.readouterr()

    assert (
        f'Searching tickets for {controller.search_term} with a value of {controller.search_value}'
    ) in captured.out

    assert '_id' in captured.out
    assert 'url' in captured.out
    assert 'external_id' in captured.out
    assert 'created_at' in captured.out
    assert 'type' in captured.out
    assert 'subject' in captured.out
    assert 'description' in captured.out
    assert 'priority' in captured.out
    assert 'status' in captured.out
    assert 'submitter_id' in captured.out
    assert 'submitter_name' in captured.out
    assert 'assignee_id' in captured.out
    assert 'assignee_name' in captured.out
    assert 'organization_id' in captured.out
    assert 'orgnaization_name' in captured.out
    assert 'tags' in captured.out
    assert 'has_incidents' in captured.out
    assert 'due_at' in captured.out
    assert 'via' in captured.out


@pytest.mark.django_db
def test_search_tickets_for_no_data(capsys):
    controller = AppController()
    controller.search_term = '_id'
    controller.search_value = 1
    controller.search = Search(controller.search_term, controller.search_value)
    controller.search_tickets()

    captured = capsys.readouterr()

    assert (
        f'No results found for search term {controller.search_term} '
        f'and search value {controller.search_value}'
    ) in captured.out


@pytest.mark.django_db
def test_search_tickets_for_invalid_search_term(capsys):
    controller = AppController()
    controller.search_term = 'unknown'
    controller.search_value = 1
    controller.search = Search(controller.search_term, controller.search_value)
    controller.search_tickets()

    captured = capsys.readouterr()

    assert f'Invalid search term "{controller.search_term}"' in captured.out
