import pytest

from search.factory import OrganizationFactory, TicketFactory, UserFactory
from search.models import User
from search.views import InvalidSearchTermException, Search


@pytest.mark.django_db
def test_user_search_for_no_matching_data():
    user = UserFactory()
    search = Search(search_term='_id', search_value=user._id+1)
    qs = search.search_users()
    assert len(qs) == 0


@pytest.mark.django_db
def test_user_search_for_no_data():
    search = Search(search_term='_id', search_value=1)
    qs = search.search_users()
    assert len(qs) == 0


@pytest.mark.django_db
def test_user_search_returns_data_only_for_the_requested_search_value():
    UserFactory()
    UserFactory()
    user = UserFactory()

    search = Search(search_term='_id', search_value=user._id)
    qs = search.search_users()

    assert len(qs) == 1
    assert qs[0]._id == user._id
    assert qs[0].url == user.url
    assert qs[0].external_id == user.external_id
    assert qs[0].name == user.name
    assert qs[0].alias == user.alias
    assert qs[0].created_at == user.created_at
    assert qs[0].active == user.active
    assert qs[0].verified == user.verified
    assert qs[0].shared == user.shared
    assert qs[0].locale == user.locale
    assert qs[0].timezone == user.timezone
    assert qs[0].last_login_at == user.last_login_at
    assert qs[0].email == user.email
    assert qs[0].phone == user.phone
    assert qs[0].signature == user.signature
    assert qs[0].organization_id == user.organization_id
    assert qs[0].tags == user.tags
    assert qs[0].suspended == user.suspended
    assert qs[0].role == user.role
    assert qs[0].submitted_tickets.count() == 0
    assert qs[0].assigned_tickets.count() == 0


@pytest.mark.django_db
def test_user_search_returns_all_data_matching_requested_search_value():
    for _ in range(3):
        UserFactory(role='admin')

    search = Search(search_term='role', search_value='admin')
    qs = search.search_users()

    assert len(qs) == 3
    assert qs[0].role == 'admin'
    assert qs[1].role == 'admin'
    assert qs[2].role == 'admin'


@pytest.mark.django_db
def test_user_search_returns_data_partially_matching_requested_search_value():
    UserFactory(role='admin')

    search = Search(search_term='role', search_value='adm')
    qs = search.search_users()

    assert len(qs) == 1
    assert qs[0].role == 'admin'


@pytest.mark.django_db
def test_user_search_is_case_insensitive():
    UserFactory(role='admin')

    search = Search(search_term='role', search_value='ADMIN')
    qs = search.search_users()

    assert len(qs) == 1
    assert qs[0].role == 'admin'


@pytest.mark.django_db
def test_user_search_returns_ticket_objects_assigned_to_user():
    user = UserFactory()
    for _ in range(3):
        TicketFactory(assignee_id=user)

    search = Search(search_term='_id', search_value=user._id)
    qs = search.search_users()

    assert len(qs) == 1
    assert qs[0]._id == user._id
    assert qs[0].assigned_tickets.count() == 3


@pytest.mark.django_db
def test_user_search_does_not_return_tickets_when_no_tickets_are_assigned_to_user():
    user = UserFactory()
    for _ in range(3):
        TicketFactory()

    search = Search(search_term='_id', search_value=user._id)
    qs = search.search_users()

    assert len(qs) == 1
    assert qs[0]._id == user._id
    assert qs[0].assigned_tickets.count() == 0


@pytest.mark.django_db
def test_user_search_returns_ticket_objects_submitted_by_user():
    user = UserFactory()
    for _ in range(3):
        TicketFactory(submitter_id=user)

    search = Search(search_term='_id', search_value=user._id)
    qs = search.search_users()

    assert len(qs) == 1
    assert qs[0]._id == user._id
    assert qs[0].submitted_tickets.count() == 3


@pytest.mark.django_db
def test_user_search_does_not_return_tickets_when_no_tickets_are_submitted_by_user():
    user = UserFactory()
    for _ in range(3):
        TicketFactory()

    search = Search(search_term='_id', search_value=user._id)
    qs = search.search_users()

    assert len(qs) == 1
    assert qs[0]._id == user._id
    assert qs[0].submitted_tickets.count() == 0


@pytest.mark.django_db
def test_user_search_raises_exception_for_invalid_search_term():
    with pytest.raises(InvalidSearchTermException) as e:
        search = Search(search_term='hello', search_value='web')
        search.search_users()
    assert str(e.value) == 'Invalid search term "hello" for users search.'


@pytest.mark.django_db
def test_user_search_using_foreign_key_organization_id_as_search_term():
    user = UserFactory()

    search = Search(search_term='organization_id', search_value=user.organization_id._id)
    qs = search.search_users()

    assert len(qs) == 1
    assert qs[0].organization_id._id == user.organization_id._id
