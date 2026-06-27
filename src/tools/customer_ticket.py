from langchain.tools import tool, ToolRuntime
from src.schemas.schemas import UserContext
from src.services.ticket_service import TicketService

@tool("getTicketByCustomerEmail")
def get_tickets_by_customer_email(
    runtime: ToolRuntime[UserContext],
    customer_email: str | None = None,
    offset: int = 0,
    limit: int = 5,
):
  

    """
    Retrieve support tickets for a customer.

    This is a READ-ONLY tool. It retrieves support tickets and never modifies data.

    Use this tool whenever the user requests:
    - Show my support tickets.
    - View my tickets.
    - Check my ticket status.
    - List my tickets.
    - Show open, closed, pending, or resolved tickets.
    - Retrieve ticket history.
    - Show tickets for a specific customer email.

    Access Control
    --------------
    - Admin:
    - Can retrieve tickets for any customer.
    - Must use the email address explicitly provided in the user's request.

    - Manager:
    - Can retrieve tickets for customers they are authorized to access.
    - Must use the email address explicitly provided in the user's request.

    - Customer:
    - Can retrieve ONLY their own tickets.
    - NEVER use an email address mentioned in the user's message.
    - ALWAYS use runtime.context.customer_email.

    Email Selection Rules
    ---------------------
    - If role == "customer":
        customer_email = runtime.context.customer_email

    - If role == "admin" or role == "manager":
        Use the customer email explicitly mentioned in the user's request.
        If no customer email is provided, ask the user for one.

    Never substitute, guess, or partially match an email address.

    If no tickets are found:
    - Return that no tickets were found.
    - Do NOT fabricate ticket IDs or ticket details.

    If the customer attempts to access another customer's tickets:
    Raise:

    PermissionError(
        "Access denied. You are authorized to view only your own ticket information."
    )

    Args:
        runtime:
            Authenticated user's runtime context.

        customer_email:
            Customer email to search.
            Required for Admin and Manager.
            Ignored for Customer because runtime.context.customer_email is always used.

        offset:
            Pagination offset.

        limit:
            Number of records to return.

    Returns:
        list[dict]:
            Support ticket information.
    """
    print(">>> getTicketByCustomerEmail CALLED <<<") 
    print("Searching email:", customer_email)
    
 

    logged_in_email = str(runtime.context.customer_email).strip().lower()
    user_role = str(runtime.context.role).strip().lower()

    if user_role == "customer":
        if (
            customer_email is not None
            and customer_email.strip().lower() != logged_in_email
        ):
            raise PermissionError(
                "Access denied. Customers are authorized to access only their own ticket information."
            )

        customer_email = logged_in_email

    elif customer_email is None:
        raise ValueError(
            "Customer email is required for administrators and managers."
        )

    # THIS LINE MUST EXIST
    tickets = TicketService.get_tickets_by_customer_email(
        customer_email=customer_email,
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
            "issue_description": ticket.issue_description,
            "ticket_created_date": ticket.ticket_created_date,
        }
        for ticket in tickets
    ]