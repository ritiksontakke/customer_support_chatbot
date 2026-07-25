from typing import Optional

from langchain.tools import tool, ToolRuntime

from src.schemas.schemas import UserContext
from src.services.ticket_service import TicketService


@tool("GetChannels")
def getChannel(
    runtime: ToolRuntime[UserContext],
    channel: Optional[str] = None,
    customer_email: Optional[str] = None,
    offset: int = 0,
    limit: int = 5,
):
    """
    Retrieve customer ticket channels with role-based authorization.

    This tool returns the communication channel (e.g., Email, Phone, Chat, Web)
    associated with support tickets. By default, only the 5 most recent tickets
    are returned unless `offset` or `limit` is specified.

    Role-Based Access
    -----------------
    Customer
    - Can view only their own ticket channels.
    - If `customer_email` is provided and does not match the logged-in user's
      email, access is denied.
    - If no email is provided, the logged-in customer's email is used automatically.

    Admin / Manager
    - Can view ticket channels for any customer.
    - If `customer_email` is omitted, the logged-in user's email is used.
    - Can search using another customer's email.

    Supported User Queries
    ----------------------
    General queries:
    - Show my channel
    - Show my channels
    - Show my recent channels
    - What are my ticket channels?
    - Show channel for ritikson@gmail.com
    - Show channels for customer ritikson@gmail.com

    Filter by channel:
    - Show my Email tickets
    - Show my Phone tickets
    - Show my Chat tickets
    - Show my Web tickets
    - Show Email channel tickets for ritikson@gmail.com

    Query using Ticket ID:
    - Show the channel for ticket ID 2
    - What is the channel of ticket 2?
    - Ticket ID 2 channel
    - Show channel name for ticket 2

    Typo Tolerance
    --------------
    The agent should interpret common spelling mistakes for "channel", such as:
    - chennel
    - chennal
    - chanal
    - chanal
    - chanel
    - chanle

    These variations should be treated as "channel" whenever the user's intent
    is clear.

    Response
    --------
    Returns a list containing:
    - ticket_id : Unique ticket identifier.
    - channel   : Communication channel for the ticket.

    Example Response:
    [
        {
            "ticket_id": 2,
            "channel": "Email"
        },
        {
            "ticket_id": 5,
            "channel": "Phone"
        }
    ]

    Authorization Errors
    --------------------
    If a customer attempts to access another customer's information, return:

        Access denied. Customers are authorized to view only their own support tickets.

    Example:
    User (logged in as abc@gmail.com):
        Show channels for ritik@gmail.com

    Response:
        Access denied. Customers are authorized to view only their own support tickets.

    Notes
    -----
    - By default, the tool returns only the latest 5 tickets.
    - Supports pagination through `offset` and `limit`.
    - Customers can access only their own ticket information.
    - Admins and Managers can access ticket channel information for any customer.
    - Channel matching should be case-insensitive.
    - User queries containing minor spelling mistakes for "channel" should still
      be understood when the intent is unambiguous.
    """

    print("GetByChannel")

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
            return {
                "success": False,
                "message":" Customers are authorized to view only their own support tickets."
            }

        search_email = logged_in_email

    elif role in {"admin", "manager"}:

        search_email = customer_email or logged_in_email

    else:
        return {
            "success": False,
            "message": "Access denied. Your account does not have permission to access customer ticket information."
        }

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

    tickets = TicketService.getchannels(
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