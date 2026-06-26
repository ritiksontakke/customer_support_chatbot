from langchain.tools import tool, ToolRuntime
from src.schemas.schemas import UserContext
from src.services.ticket_service import TicketService

@tool("GetTicketStatus")
def get_tickets_by_customer_email_and_status(
    runtime: ToolRuntime[UserContext],
    status: str,
    offset: int = 0,
    limit: int = 5,
):
    """
    Get the most recent support tickets for an authenticated customer filtered by ticket status.

    Use this tool whenever a customer:
    - asks about their closed tickets
    - asks about their open tickets
    - asks about their in-progress tickets
    - asks "Tell me about my recent closed tickets"
    - asks "Show my latest open tickets"
    - asks "What in-progress tickets do I have?"
    - asks "Tell me about my recent tickets which are closed/open/in-progress"

    This is a READ-ONLY tool.

    The tool searches customer ticket data stored in Supabase and returns
    the customer's most recent tickets matching the requested status.

    Returns up to 5 tickets ordered from newest to oldest.
    """

    customer_email = runtime.context.customer_email

    tickets = TicketService.get_tickets_by_customer_email_and_status(
        customer_email=customer_email,
        status=status,
        offset=offset,
        limit=limit,
    )

    return [
        {
            "ticket_id": ticket.ticket_id,
            "product": ticket.product,
            "category": ticket.category,
            "issue_description": ticket.issue_description,
            "priority": ticket.priority,
            "status": ticket.status,
            "channel": ticket.channel,
            "ticket_created_date": ticket.ticket_created_date,
        }
        for ticket in tickets
    ]