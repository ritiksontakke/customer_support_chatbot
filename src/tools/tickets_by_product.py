from langchain.tools import tool, ToolRuntime
from src.schemas.schemas import UserContext
from src.services.ticket_service import TicketService

@tool("GetTicketsByProduct")
def get_tickets_by_product(
    runtime: ToolRuntime[UserContext],
    product: str,
    offset: int = 0,
    limit: int = 5,
):
    """
    Get customer support tickets for a specific product.

    Use this tool whenever a customer:
    - asks "Tell me the tickets I have raised for my cloud service"
    - asks "Show my web service tickets"
    - asks "What tickets have I raised for product X?"
    - asks about tickets related to a specific product

    This is a READ-ONLY tool.

    The tool searches customer ticket data stored in Supabase and
    returns tickets belonging to the authenticated customer that
    are associated with the requested product.

    Returns matching customer tickets.
    """

    customer_email = runtime.context.customer_email

    tickets = TicketService.get_tickets_by_product(
        customer_email=customer_email,
        product=product,
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
            "ticket_created_date": ticket.ticket_created_date,
        }
        for ticket in tickets
    ]