from langchain.tools import tool

from src.services.ticket_service import TicketService


@tool("CreateTicket")
def create_ticket(
    customer_name: str,
    customer_email: str,
    subject: str,
    description: str,
    product: str,
    channel: str,
    priority: str = "Medium",
):
    """
    Create a new customer support ticket.
    """

    return TicketService.create_ticket(
        customer_name=customer_name,
        customer_email=customer_email,
        subject=subject,
        description=description,
        product=product,
        channel=channel,
        priority=priority,
    )