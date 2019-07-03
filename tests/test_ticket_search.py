import pytest

from search.factory import TicketFactory
from search.views import InvalidSearchTermException, Search


@pytest.mark.django_db
def test_ticket_search_for_no_matching_data():
    TicketFactory(_id='ticket 1')
    search = Search(search_term='_id', search_value='No Match')
    qs = search.search_tickets()
    assert len(qs) == 0


@pytest.mark.django_db
def test_ticket_search_for_no_data():
    search = Search(search_term='_id', search_value=1)
    qs = search.search_tickets()
    assert len(qs) == 0


@pytest.mark.django_db
def test_ticket_search_returns_data_only_for_the_requested_search_value():
    TicketFactory()
    TicketFactory()
    ticket = TicketFactory()

    search = Search(search_term='_id', search_value=ticket._id)
    qs = search.search_tickets()

    assert len(qs) == 1
    assert qs[0]._id == ticket._id
    assert qs[0].url == ticket.url
    assert qs[0].external_id == ticket.external_id
    assert qs[0].created_at == ticket.created_at
    assert qs[0].type == ticket.type
    assert qs[0].subject == ticket.subject
    assert qs[0].description == ticket.description
    assert qs[0].priority == ticket.priority
    assert qs[0].status == ticket.status
    assert qs[0].submitter_id == ticket.submitter_id
    assert qs[0].assignee_id == ticket.assignee_id
    assert qs[0].organization_id == ticket.organization_id
    assert qs[0].tags == ticket.tags
    assert qs[0].has_incidents == ticket.has_incidents
    assert qs[0].due_at == ticket.due_at
    assert qs[0].via == ticket.via


@pytest.mark.django_db
def test_ticket_search_returns_all_data_matching_requested_search_value():
    for _ in range(3):
        TicketFactory(via='web')

    search = Search(search_term='via', search_value='web')
    qs = search.search_tickets()

    assert len(qs) == 3
    assert qs[0].via == 'web'
    assert qs[1].via == 'web'
    assert qs[2].via == 'web'


@pytest.mark.django_db
def test_ticket_search_returns_data_partially_matching_requested_search_value():
    TicketFactory(via='web')

    search = Search(search_term='via', search_value='we')
    qs = search.search_tickets()

    assert len(qs) == 1
    assert qs[0].via == 'web'


@pytest.mark.django_db
def test_ticket_search_is_case_insensitive():
    TicketFactory(via='web')

    search = Search(search_term='via', search_value='WEB')
    qs = search.search_tickets()

    assert len(qs) == 1
    assert qs[0].via == 'web'


@pytest.mark.django_db
def test_ticket_search_raises_exception_for_invalid_search_term():
    with pytest.raises(InvalidSearchTermException) as e:
        search = Search(search_term='hello', search_value='web')
        search.search_tickets()
    assert str(e.value) == 'Invalid search term "hello" for tickets search.'


@pytest.mark.django_db
def test_ticket_search_using_foreign_key_organization_id_as_search_term():
    ticket = TicketFactory()

    search = Search(search_term='organization_id', search_value=ticket.organization_id._id)
    qs = search.search_tickets()

    assert len(qs) == 1
    assert qs[0].organization_id._id == ticket.organization_id._id


@pytest.mark.django_db
def test_ticket_search_using_foreign_key_submitter_id_as_search_term():
    ticket = TicketFactory()

    search = Search(search_term='submitter_id', search_value=ticket.submitter_id._id)
    qs = search.search_tickets()

    assert len(qs) == 1
    assert qs[0].submitter_id._id == ticket.submitter_id._id


@pytest.mark.django_db
def test_ticket_search_using_foreign_key_assignee_id_as_search_term():
    ticket = TicketFactory()

    search = Search(search_term='assignee_id', search_value=ticket.assignee_id._id)
    qs = search.search_tickets()

    assert len(qs) == 1
    assert qs[0].assignee_id._id == ticket.assignee_id._id
