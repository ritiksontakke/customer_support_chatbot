from typing import Optional

from langchain.tools import tool, ToolRuntime

from src.schemas.schemas import UserContext
from src.services.ticket_service import TicketService


@tool("GetTicketsByChannel")
def get_tickets_by_channel(
    runtime: ToolRuntime[UserContext],
    channel: str,
    customer_email: Optional[str] = None,
    offset: int = 0,
    limit: int = 5,
):
    """
    Retrieve customer support tickets filtered by their ticket creation channel.

    This is a READ-ONLY tool.

    A ticket channel is the source through which the ticket was created.

    Examples of channels:
    - Phone
    - Email
    - Web Portal
    - Mobile App
    - Chat

    Use this tool ONLY when the user specifies a ticket creation channel.

    Examples:
    - Show my Phone tickets.
    - List my Email tickets.
    - Show tickets raised through Web Portal.
    - Show my Mobile App tickets.
    - Show Chat tickets for ritiksontakke@gmail.com. (Manager/Admin)

    Do NOT use this tool for generic questions such as:
    - Show my channel.
    - What is my channel?
    - Which channel am I using?

    In those cases, ask the user to specify the ticket creation channel.

    Role Permissions
    ----------------
    Customer
    - Can retrieve only their own tickets.

    Manager
    - Can retrieve tickets for any customer.

    Admin
    - Full access to all customer tickets.
    """

    print("GetTicketsByChannel")

    user = runtime.context

    role = user.role.lower()
    logged_in_email = user.customer_email

    # Authorization
    if role == "customer":
        if (
            customer_email
            and customer_email.lower() != logged_in_email.lower()
        ):
            raise PermissionError(
                "Access denied. Customers are authorized to view only their own support tickets."
            )

        search_email = logged_in_email

    elif role in {"admin", "manager"}:
        search_email = customer_email or logged_in_email

    else:
        raise PermissionError(
            "Access denied. Your account does not have permission to access customer ticket information."
        )

    tickets = TicketService.get_tickets_by_channel(
        customer_email=search_email,
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