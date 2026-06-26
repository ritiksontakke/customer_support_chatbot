from langchain.tools import tool, ToolRuntime
from src.schemas.schemas import UserContext
from src.services.ticket_service import TicketService

@tool("getTicketByCustomerEmail")
def get_tickets_by_customer_email(
    runtime: ToolRuntime[UserContext],
    offset: int = 0,
    limit: int = 5,
):
    """
    Retrieve the most recent support tickets for the authenticated customer.

    Use this tool when a customer asks:
    - Tell me about my recent tickets
    - Show my latest tickets
    - Show my support history
    - What support requests have I opened?

    This is a READ-ONLY tool.

    The tool searches the customer_support_tickets table using the
    authenticated customer's email address and returns the most
    recent tickets ordered by newest first.

    Returns up to 5 tickets by default.
    """

    customer_email = runtime.context.customer_email

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