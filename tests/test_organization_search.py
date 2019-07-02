import pytest

from search.factory import OrganizationFactory, TicketFactory, UserFactory
from search.models import Organization
from search.views import InvalidSearchTermException, Search


@pytest.mark.django_db
def test_organization_search_for_no_matching_data():
    organization = OrganizationFactory()
    search = Search(search_term='_id', search_value=organization._id+1)
    qs = search.search_organizations()
    assert len(qs) == 0


@pytest.mark.django_db
def test_organization_search_for_no_data():
    search = Search(search_term='_id', search_value=1)
    qs = search.search_organizations()
    assert len(qs) == 0


@pytest.mark.django_db
def test_organization_search_returns_data_only_for_the_requested_search_value():
    OrganizationFactory()
    OrganizationFactory()
    organization = OrganizationFactory()

    search = Search(search_term='_id', search_value=organization._id)
    qs = search.search_organizations()

    assert len(qs) == 1
    assert qs[0]._id == organization._id
    assert qs[0].url == organization.url
    assert qs[0].external_id == organization.external_id
    assert qs[0].name == organization.name
    assert qs[0].domain_names == organization.domain_names
    assert qs[0].created_at == organization.created_at
    assert qs[0].details == organization.details
    assert qs[0].shared_tickets == organization.shared_tickets
    assert qs[0].tags == organization.tags


@pytest.mark.django_db
def test_organization_search_returns_all_data_matching_requested_search_value():
    for _ in range(3):
        OrganizationFactory(details='MegaCorp')

    search = Search(search_term='details', search_value='MegaCorp')
    qs = search.search_organizations()

    assert len(qs) == 3
    assert qs[0].details == 'MegaCorp'
    assert qs[1].details == 'MegaCorp'
    assert qs[2].details == 'MegaCorp'


@pytest.mark.django_db
def test_organization_search_returns_data_partially_matching_requested_search_value():
    OrganizationFactory(details='MegaCorp')

    search = Search(search_term='details', search_value='corp')
    qs = search.search_organizations()

    assert len(qs) == 1
    assert qs[0].details == 'MegaCorp'


@pytest.mark.django_db
def test_organization_search_is_case_insensitive():
    OrganizationFactory(details='MegaCorp')

    search = Search(search_term='details', search_value='megacorp')
    qs = search.search_organizations()

    assert len(qs) == 1
    assert qs[0].details == 'MegaCorp'


@pytest.mark.django_db
def test_organization_search_returns_linked_user_and_ticket_objects():
    organization = OrganizationFactory()
    for _ in range(2):
        UserFactory(organization_id=organization)
    for _ in range(3):
        TicketFactory(organization_id=organization)

    search = Search(search_term='_id', search_value=organization._id)
    qs = search.search_organizations()

    assert len(qs) == 1
    assert qs[0]._id == organization._id
    assert qs[0].users.count() == 2
    assert qs[0].tickets.count() == 3


@pytest.mark.django_db
def test_organization_search_does_not_return_user_and_ticket_objects_when_not_linked():
    organization = OrganizationFactory()
    for _ in range(2):
        UserFactory()
    for _ in range(3):
        TicketFactory()

    search = Search(search_term='_id', search_value=organization._id)
    qs = search.search_organizations()

    assert len(qs) == 1
    assert qs[0]._id == organization._id
    assert qs[0].users.count() == 0
    assert qs[0].tickets.count() == 0


@pytest.mark.django_db
def test_organization_search_retrieves_data_when_value_is_blank():
    OrganizationFactory(name='')

    search = Search(search_term='name', search_value='')
    qs = search.search_organizations()

    assert len(qs) == 1
    assert qs[0].name == ''


@pytest.mark.django_db
def test_organization_search_for_a_character_field_lookup():
    OrganizationFactory(name='testName')

    search = Search(search_term='name', search_value='testName')
    qs = search.search_organizations()

    assert len(qs) == 1
    assert qs[0].name == 'testName'


@pytest.mark.django_db
def test_organization_search_for_a_boolean_field_lookup():
    OrganizationFactory(shared_tickets='true')

    search = Search(search_term='shared_tickets', search_value='true')
    qs = search.search_organizations()

    assert len(qs) == 1
    assert qs[0].shared_tickets == 'true'


@pytest.mark.django_db
def test_organization_search_for_a_list_field_lookup():
    OrganizationFactory(
        domain_names='["kage.com", "ecratic.com", "endipin.com", "zentix.com"]'
    )

    search = Search(search_term='domain_names', search_value='kage')
    qs = search.search_organizations()

    assert len(qs) == 1
    assert qs[0].domain_names == '["kage.com", "ecratic.com", "endipin.com", "zentix.com"]'


@pytest.mark.django_db
def test_organization_search_raises_exception_for_invalid_search_term():
    with pytest.raises(InvalidSearchTermException) as e:
        search = Search(search_term='hello', search_value='web')
        search.search_organizations()
    assert str(e.value) == 'Invalid search term "hello"'
