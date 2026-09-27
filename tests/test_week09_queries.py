# tests/test_week09_queries.py
import pytest

from app.models.entities import User
from app.models.enums import Role, TicketStatus
from app.services.tickets import TicketService


def create_ticket(service, title, category, requester_id=1):
    return service.create(
        title=title,
        description="Caso de prueba",
        category=category,
        priority="Medium",
        requester_id=requester_id,
    )


@pytest.fixture
def technician():
    return User(id=10, name="Tomas", email="tomas@school.edu", role=Role.TECHNICIAN)


# ---------- list_by_technician: que tickets tiene asignados este tecnico? ----------

def test_list_by_technician_returns_only_assigned_tickets():
    service = TicketService()
    first = create_ticket(service, "No imprime", "Hardware")
    second = create_ticket(service, "No ingresa", "Software")
    service.assign_technician(ticket_id=first.id, technician_id=10)
    service.assign_technician(ticket_id=second.id, technician_id=20)

    result = service.list_by_technician(10)

    assert result == [first]
    assert second not in result


def test_list_by_technician_returns_all_tickets_of_that_technician():
    service = TicketService()
    a = create_ticket(service, "No imprime", "Hardware")
    b = create_ticket(service, "Monitor sin senal", "Hardware")
    c = create_ticket(service, "No ingresa", "Software")
    service.assign_technician(ticket_id=a.id, technician_id=10)
    service.assign_technician(ticket_id=b.id, technician_id=10)
    service.assign_technician(ticket_id=c.id, technician_id=20)

    assert service.list_by_technician(10) == [a, b]


def test_list_by_technician_ignores_unassigned_tickets():
    service = TicketService()
    create_ticket(service, "Sin asignar", "General")

    assert service.list_by_technician(99) == []


def test_list_by_technician_follows_reassignment():
    service = TicketService()
    ticket = create_ticket(service, "No imprime", "Hardware")
    service.assign_technician(ticket_id=ticket.id, technician_id=10)
    service.assign_technician(ticket_id=ticket.id, technician_id=20)

    assert service.list_by_technician(10) == []
    assert service.list_by_technician(20) == [ticket]


# ---------- list_by_category: que tickets pertenecen a esta categoria? ----------

def test_list_by_category_returns_only_matching_category():
    service = TicketService()
    hardware = create_ticket(service, "No imprime", "Hardware")
    create_ticket(service, "No ingresa", "Software")

    result = service.list_by_category("Hardware")

    assert result == [hardware]


def test_list_by_category_ignores_case_and_spaces():
    service = TicketService()
    hardware = create_ticket(service, "No imprime", "Hardware")

    assert service.list_by_category("  hardware ") == [hardware]


def test_list_by_category_without_tickets_returns_empty_list():
    service = TicketService()
    create_ticket(service, "No imprime", "Hardware")

    assert service.list_by_category("Network") == []


def test_list_by_category_rejects_unknown_category():
    service = TicketService()

    with pytest.raises(ValueError, match="category"):
        service.list_by_category("Cocina")


# ---------- list_by_status: que tickets siguen abiertos o en proceso? ----------

def test_list_by_status_returns_only_matching_status():
    service = TicketService()
    open_ticket = create_ticket(service, "Caso abierto", "General")

    result = service.list_by_status("open")

    assert open_ticket in result


def test_list_by_status_accepts_enum_and_uppercase_text():
    service = TicketService()
    ticket = create_ticket(service, "Caso abierto", "General")

    assert service.list_by_status(TicketStatus.OPEN) == [ticket]
    assert service.list_by_status("OPEN") == [ticket]


def test_list_by_status_separates_open_from_in_progress(technician):
    service = TicketService()
    still_open = create_ticket(service, "Caso abierto", "General")
    working = create_ticket(service, "Caso en proceso", "Hardware")
    service.change_status(working.id, TicketStatus.IN_PROGRESS, actor=technician)

    assert service.list_by_status("open") == [still_open]
    assert service.list_by_status("In Progress") == [working]


def test_list_by_status_excludes_closed_tickets(technician):
    service = TicketService()
    active = create_ticket(service, "Caso activo", "Software")
    closed = create_ticket(service, "Caso cerrado", "Software")
    service.change_status(closed.id, "closed", actor=technician)

    assert service.list_by_status("open") == [active]
    assert service.list_by_status("closed") == [closed]


def test_list_by_status_rejects_unknown_status():
    service = TicketService()

    with pytest.raises(ValueError, match="status"):
        service.list_by_status("estado_inventado")
