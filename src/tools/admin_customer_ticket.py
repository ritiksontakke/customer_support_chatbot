from langchain.tools import tool, ToolRuntime

from src.schemas.schemas import UserContext
from src.services.ticket_service import TicketService


@tool("getCustomerTicket")
def get_customer_ticket(
    runtime: ToolRuntime[UserContext],
    customer_email: str | None = None,
    offset: int = 0,
    limit: int = 5,
):
    """
    Retrieve tickets for any customer.

    Only Admin can use this tool.
    """

    if runtime.context.role.lower() != "admin":
        raise PermissionError(
            "Only Admin can access customer tickets."
        )

    tickets = TicketService.get_tickets_by_customer_email(
        customer_email=customer_email,
        offset=offset,
        limit=limit,
    )

    return [
        {
            "ticket_id": ticket.ticket_id,
            "product": ticket.product,
            "category": ticket.category,
            "status": ticket.status,
            "priority": ticket.priority,
            "channel": ticket.channel,
            "issue_description": ticket.issue_description,
            "ticket_created_date": ticket.ticket_created_date,
        }
        for ticket in tickets
    ]