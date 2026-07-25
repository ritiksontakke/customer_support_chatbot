from langchain.tools import tool, ToolRuntime

from src.schemas.schemas import UserContext
from src.services.ticket_service import TicketService


@tool("getTicketDetails")
def get_ticket_details(
    runtime: ToolRuntime[UserContext],
    ticket_id: int | None = None,
    customer_email: str | None = None,
):
    """
    Retrieve support ticket details.

    This is a READ-ONLY tool used to fetch support tickets.

    ----------------------------------------------------------------------
    AUTHORIZATION
    ----------------------------------------------------------------------

    Customer
    --------
    A customer is allowed to access ONLY tickets that belong to the
    authenticated (logged-in) email.

    Supported customer requests:

    1. "Show my tickets"
       → Returns all tickets associated with the logged-in email.

    2. "Show ticket 101"
       → Returns ticket 101 ONLY if it belongs to the logged-in email.

    3. "Show my ticket details"
       → Returns every ticket for the logged-in email.
    4. "Show my ticket ID"
        → Returns only the ticket ID(s) associated with the logged-in email.

    5. "Show my ticket IDs"
        → Returns only the list of ticket IDs associated with the logged-in email.

    Examples:

        User: Show my ticket ID
        Response:
            Ticket IDs:
            - 101
            - 105

        User: Show my ticket IDs
        Response:
            Ticket IDs:
            - 101
            - 105

    Not allowed:

    • "Show tickets for abc@gmail.com"
    • "Show ticket 101" where ticket 101 belongs to another customer.

    In both cases raise:

        PermissionError(
            "Access denied. You can only view tickets associated with your account."
        )


    ----------------------------------------------------------------------

    Admin
    -----
    Admin users can retrieve any customer's ticket(s).

    Search by:

    • ticket_id
    • customer_email
    • both

    ----------------------------------------------------------------------

    Manager
    -------
    Managers have the same read permissions as Admin.

    Search by:

    • ticket_id
    • customer_email
    • both

    ----------------------------------------------------------------------

    PARAMETERS
    ----------------------------------------------------------------------

    ticket_id : int | None

        Ticket identifier.

        Example:
            Show ticket 101

    customer_email : str | None

        Customer email.

        Example:
            Show tickets for john@gmail.com

    ----------------------------------------------------------------------

    SEARCH BEHAVIOR
    ----------------------------------------------------------------------

    Customer:

        No parameters
            -> Return ALL tickets of logged-in customer.

        ticket_id only
            -> Return that ticket ONLY if it belongs to logged-in customer.

        customer_email
            -> Ignore supplied email unless it matches logged-in email.
            "Show my ticket ID" / "Show my ticket IDs"
        -> Return only the ticket ID(s) for the logged-in customer.

        No parameters
            -> Return ALL ticket details of the logged-in customer.

        ticket_id only
            -> Return that ticket ONLY if it belongs to the logged-in customer.

    Admin / Manager:

        ticket_id
            -> Return matching ticket.

        customer_email
            -> Return all tickets for that customer.

        ticket_id + customer_email
            -> Return matching ticket after applying filters.

    ----------------------------------------------------------------------

    RETURNS
    ----------------------------------------------------------------------

    Dictionary or List[Dictionary]

    Each ticket contains:

    • ticket_id
    • customer_name
    • customer_email
    • product
    • category
    • issue_description
    • resolution_notes
    • priority
    • status
    • channel
    • ticket_created_date
    • ticket_resolved_date

    ----------------------------------------------------------------------

    RAISES
    ----------------------------------------------------------------------

    PermissionError

        If a customer attempts to access another customer's ticket.

    ValueError

        If invalid search parameters are provided.

    ----------------------------------------------------------------------

    EXAMPLES
    ----------------------------------------------------------------------

    Customer:

        Show my tickets

        Show my ticket details

        Show ticket 105
        Customer:

        Show my tickets

        Show my ticket details

        Show my ticket ID

        Show my ticket IDs

    Show ticket 105

    Admin:

        Show ticket 101

        Show tickets for john@gmail.com

        Show ticket 101 for john@gmail.com

    Manager:

        Show ticket 300

        Show tickets for alice@gmail.com
    """

    print("========== getTicketDetails ==========")
    print("Role:", runtime.context.role)
    print("Logged in Email:", runtime.context.customer_email)
    print("Requested Ticket:", ticket_id)
    print("Requested Email:", customer_email)

    logged_in_email = runtime.context.customer_email.strip().lower()
    role = runtime.context.role.strip().lower()

    # ---------------------------------------------------------
    # CUSTOMER AUTHORIZATION
    # ---------------------------------------------------------

    if role == "customer":

        # Customer cannot search another customer's email
        if (
            customer_email is not None
            and customer_email.strip().lower() != logged_in_email
        ):
            raise PermissionError(
                "Access denied. You can only view tickets associated with your account."
            )

        # Always force authenticated email
        customer_email = logged_in_email

    # ---------------------------------------------------------
    # FETCH DATA
    # ---------------------------------------------------------

    tickets = TicketService.get_ticket_details(
        ticket_id=ticket_id,
        customer_email=customer_email,
    )

    if not tickets:
        return None

    # If service returns single object convert to list
    if not isinstance(tickets, list):
        tickets = [tickets]

    results = []

    for ticket in tickets:

        # Extra safety check
        if (
            role == "customer"
            and ticket.customer_email.strip().lower() != logged_in_email
        ):
            raise PermissionError(
                "Access denied. You can only view tickets associated with your account."
            )

        results.append(
            {
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
        )

    # # Return single object when searching by ticket id
    # if ticket_id is not None and len(results) == 1:
    #     return results[0]

    return results