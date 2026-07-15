from typing import Optional
from langchain.tools import ToolRuntime, tool
from src.schemas.schemas import UserContext
from src.services.ticket_service import TicketService


@tool("GetTicketStatus")
def get_tickets_by_customer_email_and_status(
    runtime: ToolRuntime[UserContext],
    status: str,
    customer_email: Optional[str] = None,
    offset: int = 0,
    limit: int = 2,
):
    """
    Retrieve customer support tickets filtered by ticket status.

    IMPORTANT FOR THE AGENT
    -----------------------
    - Ticket ID is OPTIONAL.
    - This tool retrieves tickets using the customer's email and ticket status.
    - For authenticated Customers, always use `runtime.context.customer_email`.
    - Do NOT ask the customer for their email or Ticket ID if they are already logged in.
    - If the user says "Show my tickets", "Show my ticket status", or similar,
    use the authenticated customer's email automatically.
    - If the user provides a Ticket ID, another ticket lookup tool may be used
    to retrieve that specific ticket.
    - This tool requires a ticket status.
    - Use the status exactly as provided by the user.
    - Do NOT modify, normalize, infer, or guess the status.
    - If the user does not specify a ticket status, ask:
    "Which ticket status would you like to check? (e.g. Open, Pending, Closed, Resolved)"
    - Do NOT automatically search across multiple statuses.
    - Do NOT ask the user to confirm their role or permissions.
    The authenticated role is available in `runtime.context.role`.
    - Authorization is enforced by this tool.

    Role-Based Access
    -----------------

    Customer
    --------
    - Customers can ONLY view tickets associated with their authenticated
    login email (`runtime.context.customer_email`).
    - Ticket ID is NOT required when the customer is authenticated.
    - Always use the authenticated customer's email.
    - Any `customer_email` provided by the customer MUST be ignored if it
    differs from the authenticated email.
    - Customers are NOT allowed to view another customer's tickets.

    Example Queries:
        ✓ "What is my Open ticket status?"
        ✓ "Show my Closed tickets."
        ✓ "List my Pending support tickets."
        ✓ "Show my ticket status."

    Invalid Queries:
        ✗ "Show Open tickets for john@example.com."
        ✗ "What is the ticket status for alice@gmail.com?"

    Manager / Admin
    ---------------
    - Managers and Admins can view tickets for any customer.
    - If a customer email is provided, use that email.
    - If no customer email is provided, use the authenticated user's email
    as the default.
    - Managers/Admins may retrieve tickets for any valid customer account.

    Example Queries:
        ✓ "Show Open tickets for john@example.com."
        ✓ "What is the Closed ticket status for alice@gmail.com?"
        ✓ "List Pending tickets for bob@example.com."
        ✓ "Show my Open tickets."

    Args
    ----
    status : str
        Ticket status to filter by.

        Example values:
        - Open
        - Pending
        - Closed
        - Resolved

    customer_email : Optional[str]
        Customer email address.
        - Ignored for Customer role.
        - Used for Manager/Admin role.
        - Defaults to the authenticated user's email if omitted.

    offset : int
        Pagination offset.

    limit : int
        Maximum number of tickets to return.

    Returns
    -------
    list[dict]
        A list of ticket objects.

    Notes
    -----
    - Customers are restricted to their own authenticated account.
    - Managers and Admins may access tickets for any customer.
    - The requested status must match exactly as provided by the user.
    - Do not infer or search additional statuses.

    RESPONSE FORMAT
    ---------------
    When responding to the user:

    - Keep the response short, professional, and direct.
    - Use the status value exactly as returned by the database.
    - Do NOT modify or normalize the status.
    - Do NOT mention product, category, priority, issue description, channel, or ticket creation date.
    - Do NOT ask follow-up questions.
    - Do NOT provide additional explanations.

    If one ticket is returned:

    Ticket 1 Status: <status>

    If multiple tickets are returned:

    Ticket 1 Status: <status>

    Ticket 2 Status: <status>

    Ticket 3 Status: <status>

    Each ticket must start on a new line.

    If no tickets are found:

    No matching tickets were found.
    """
    print("getticketddocs str")

    # Customer -> always use authenticated user's email.
    # Manager/Admin -> use provided email if available.
    if runtime.context.role.lower() == "customer":
        # Customer can only access their own tickets.
        if (
            customer_email
            and customer_email.lower() != runtime.context.customer_email.lower()
        ):
            raise PermissionError(
                "Access denied. Customers are authorized to view only their own support tickets. "
                "Please remove the customer email or use your registered account to access your ticket information."
            )

        customer_email = runtime.context.customer_email

    else:
        # Manager/Admin
        customer_email = customer_email or runtime.context.customer_email
    
    tickets = TicketService.get_tickets_by_customer_email_and_status(
    customer_email=customer_email,
    status=status,
    offset=offset,
    limit=limit,
)

    return [
        {
            "ticket_id": ticket.ticket_id,
            "status": ticket.status,
        }
        for ticket in tickets
    ]