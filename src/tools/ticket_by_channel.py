from langchain.tools import tool, ToolRuntime
from src.schemas.schemas import UserContext
from src.services.ticket_service import TicketService

@tool("GetTicketsByChannel")
def get_tickets_by_channel(
    runtime: ToolRuntime[UserContext],
    channel: str,
    offset: int = 0,
    limit: int = 5,
):
    """
    Get customer support tickets raised through a specific channel.

    Use this tool whenever a customer:
    - asks "Tell me the tickets I raised from my phone"
    - asks "Show my mobile tickets"
    - asks "Show tickets raised through Web Portal"
    - asks about tickets created through a specific channel

    This is a READ-ONLY tool.

    The tool searches customer ticket data stored in Supabase and
    returns tickets belonging to the authenticated customer that
    were raised through the requested channel.

    Returns the most recent matching tickets.
    """

    customer_email = runtime.context.customer_email

    tickets = TicketService.get_tickets_by_channel(
        customer_email=customer_email,
        channel=channel,
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