from typing import Optional

from langchain.tools import tool, ToolRuntime

from src.schemas.schemas import UserContext
from src.services.ticket_service import TicketService


@tool("GetTicketChannels")
def get_tickets_by_channel(
    runtime: ToolRuntime[UserContext],
    channel: Optional[str] = None,
    customer_email: Optional[str] = None,
    offset: int = 0,
    limit: int = 5,
):
    """
    Retrieve support ticket channel information.

    This is a READ-ONLY tool.

    This tool supports two types of queries:

    -----------------------------------------------------------------------
    1. Generic Channel Queries (No channel specified)
    -----------------------------------------------------------------------

    Customer Examples:
    - Show my channel
    - Show my channels
    - List my channels
    - What are my ticket channels?

    Manager/Admin Examples:
    - Show the channel ritiksontakke1008@gmail.com
    - Show channels for ritiksontakke1008@gmail.com

    In these cases, return the latest tickets containing only:

    - ticket_id
    - channel

    -----------------------------------------------------------------------
    2. Channel Filter Queries (Channel specified)
    -----------------------------------------------------------------------

    Examples:

    - Show my Email tickets
    - Show my Phone tickets
    - Show my Chat tickets
    - Show Web Portal tickets
    - Show Mobile App tickets
    - Show Email tickets for ritiksontakke1008@gmail.com

    Supported channels include:

    - Email
    - Phone
    - Chat
    - Mobile App
    - Web Portal

    In these cases, return complete ticket information filtered by the
    specified ticket creation channel.

    -----------------------------------------------------------------------
    Role Permissions
    -----------------------------------------------------------------------

    Customer
    - Can retrieve only their own tickets.

    Manager
    - Can retrieve their own tickets.
    - Can retrieve tickets for any customer.

    Admin
    - Full access to all customer tickets.
    """

    print("GetTicketsByChannel")

    user = runtime.context

    role = user.role.lower()
    logged_in_email = user.customer_email

    # -------------------------
    # Authorization
    # -------------------------

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

    # ------------------------------------------------------------------
    # CASE 1 : Generic query
    # Example:
    # show my channel
    # show my channels
    # show the channel abc@gmail.com
    # ------------------------------------------------------------------

    if channel is None or channel.strip() == "":

        tickets = TicketService.get_ticket_channels(
            customer_email=search_email,
            offset=offset,
            limit=limit,
        )

        return [
            {
                "ticket_id": ticket.ticket_id,
                "channel": ticket.channel,
            }
            for ticket in tickets
        ]

    # ------------------------------------------------------------------
    # CASE 2 : Filter by channel
    # Example:
    # show my Email tickets
    # show my Phone tickets
    # ------------------------------------------------------------------

    tickets = TicketService.get_ticket_channels(
        customer_email=search_email,
        channel=channel,
        offset=offset,
        limit=limit,
    )

    return [
        {
            "ticket_id": ticket.ticket_id,
            "channel": ticket.channel,
        }
        for ticket in tickets
    ]