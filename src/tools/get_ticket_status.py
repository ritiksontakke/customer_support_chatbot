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
    limit: int = 5,
):
    """
    Retrieve customer support tickets filtered by status.
    IMPORTANT FOR THE AGENT
    -----------------------
    - This tool requires a ticket status.
    - Use the status exactly as requested by the user. Do not modify, infer, or guess the status.
    - If the user does not specify a ticket status, ask which ticket status they want to check.
    - Do not automatically search multiple statuses.
    - Do not ask the user to confirm their role or permissions. The authenticated role is available in runtime.context.role.
    - Authorization is enforced by this tool.

    Role-Based Access:
    ------------------
    Customer:
        - Can only access their own tickets.
        - The authenticated user's email (runtime.context.customer_email)
          is always used.
        - Any customer_email passed to this tool is ignored.

        Example User Query:
            - "What is my open ticket status?"
            - "Show my closed tickets."
            - "List my pending support tickets."

    Manager/Admin:
        - Can access tickets for any customer.
        - Must provide the customer's email address.
        - If customer_email is not provided, the authenticated user's email
          is used as a fallback.

        Example User Query:
            - "Show open tickets for ritiksontakke@gmail.com."
            - "What is the ticket status for john@example.com?"
            - "List closed tickets for alice@gmail.com."

    Args:
        status (str):
            Ticket status to filter by (e.g. Open, Pending, Closed, Resolved).

        customer_email (Optional[str]):
            Customer email address.
            - Ignored for Customer role.
            - Used for Manager/Admin role.

        offset (int):
            Pagination offset. Default is 0.

        limit (int):
            Maximum number of tickets to return. Default is 5.

    Returns:
        list[dict]:
            A list of ticket details containing:
            - ticket_id
            - product
            - category
            - issue_description
            - priority
            - status
            - channel
            - ticket_created_date
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