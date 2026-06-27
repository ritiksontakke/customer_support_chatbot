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
    Retrieve complete details for a support ticket.

    This is a READ-ONLY tool.

    Authorization Rules
    -------------------
    - Admin:
        Can retrieve ticket details using either ticket ID or customer email.

    - Manager:
        Can retrieve ticket details using either ticket ID or customer email.

    - Customer:
        Can retrieve only their own ticket details. If a customer provides
        another customer's email address, access is denied.

    Search Criteria
    ---------------
    - ticket_id
    - customer_email

    At least one of the above parameters must be provided.

    Examples
    --------
    - Show ticket 101
    - Show details for ticket 101
    - Show ticket details for ritiksontakke10@gmail.com
    - Find ticket using customer email

    Raises
    ------
    PermissionError:
        If a customer attempts to access another customer's ticket.

    ValueError:
        If neither ticket_id nor customer_email is provided.
    """
    print("=== getTicketDetails called ===")
    print("Role:", runtime.context.role)
    print("Logged in:", runtime.context.customer_email)
    print("ticket_id:", ticket_id)
    print("customer_email:", customer_email)

    logged_in_email = str(runtime.context.customer_email).strip().lower()
    user_role = str(runtime.context.role).strip().lower()

    # Customer authorization
    if user_role == "customer":
        # If customer tries to search another email, deny access
        if (
            customer_email
            and customer_email.strip().lower() != logged_in_email
        ):
            raise PermissionError(
                "Access denied. Customers are authorized to access only their own ticket information."
            )

        # Always use the authenticated email
        customer_email = logged_in_email

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