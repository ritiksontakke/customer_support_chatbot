from langchain.tools import tool, ToolRuntime
from src.schemas.schemas import UserContext
from src.services.ticket_service import TicketService

@tool("getTicketDetails")
def get_ticket_details(
    runtime: ToolRuntime[UserContext],
    ticket_id: int,
):
    """
    Get complete details for a specific customer support ticket.

    Use this tool whenever a customer:
    - asks for ticket details
    - provides a ticket ID
    - asks "Tell me about ticket 101"
    - asks "Show details for ticket 101"
    - asks "What is the status of ticket 101?"

    This is a READ-ONLY tool.

    The tool searches customer ticket data stored in Supabase and
    returns complete information for the requested ticket.

    Only tickets belonging to the authenticated customer should be returned.

    Returns a single ticket record.
    """

    customer_email = runtime.context.customer_email

    ticket = TicketService.get_ticket_details(
        ticket_id=ticket_id,
        customer_email=customer_email,
    )

    if ticket is None:
        return None

    return {
        "ticket_id": ticket.ticket_id,
        "customer_name": ticket.customer_name,
        "customer_email": ticket.customer_email,
        "product": ticket.product,
        "category": ticket.category,
        "issue_description": ticket.issue_description,
        "resolution_notes": ticket.resolution_notes,
        "priority": ticket.priority,
        "status": ticket.status,
        "channel": ticket.channel,
        "ticket_created_date": ticket.ticket_created_date,
        "ticket_resolved_date": ticket.ticket_resolved_date,
    }