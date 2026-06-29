from typing import Optional

from langchain.tools import tool, ToolRuntime
from src.schemas.schemas import UserContext
from src.services.ticket_service import TicketService


@tool("GetTicketsByProduct")
def get_tickets_by_product(
    runtime: ToolRuntime[UserContext],
    product: str,
    customer_email: Optional[str] = None,
    offset: int = 0,
    limit: int = 5,
):
    """
    Search customer support tickets for a specific product.

    Use this tool whenever the user asks about:
    - My tickets
    - Ticket status
    - Support tickets
    - Open tickets
    - Closed tickets
    - Pending tickets
    - Issues related to a product
    - Product ticket details
    - Status of a product ticket

    Always use this tool if the user's request involves support tickets for a product.

    Role-Based Access Control (RBAC)
    --------------------------------
    Customer:
    - Can retrieve ONLY their own tickets.
    - Always use the logged-in customer's email from runtime.context.customer_email.
    - Never allow a customer to retrieve another customer's tickets.
    - If a customer specifies another customer's email, return an access denied error.

    Admin / Manager:
    - Can retrieve tickets for any customer.
    - If customer_email is provided, search tickets for that customer.
    - Otherwise use the logged-in user's email.

    Args:
        product (str):
            Product name.

        customer_email (Optional[str]):
            Customer email.
            Used only for Admin and Manager.

        offset (int):
            Pagination offset.

        limit (int):
            Maximum number of records.

    Examples
    --------

    Customer Examples

    User:
    Show my Analytics Dashboard tickets.

    Action:
    GetTicketsByProduct(
        product="Analytics Dashboard"
    )

    User:
    What is the status of my CRM ticket?

    Action:
    GetTicketsByProduct(
        product="CRM"
    )

    User:
    Do I have any open tickets for Mobile App?

    Action:
    GetTicketsByProduct(
        product="Mobile App"
    )

    Admin Examples

    User:
    Show Analytics Dashboard tickets for ritiksontakke20@gmail.com.

    Action:
    GetTicketsByProduct(
        product="Analytics Dashboard",
        customer_email="ritiksontakke20@gmail.com"
    )

    User:
    What is the status of CRM tickets for john@gmail.com?

    Action:
    GetTicketsByProduct(
        product="CRM",
        customer_email="john@gmail.com"
    )

    Manager Examples

    User:
    List Printer tickets for mary@gmail.com.

    Action:
    GetTicketsByProduct(
        product="Printer",
        customer_email="mary@gmail.com"
    )
    """

    logged_in_email = runtime.context.customer_email
    role = runtime.context.role.lower()

    # RBAC
    if role == "customer":
        # Customer cannot search another user's data
        if customer_email and customer_email.lower() != logged_in_email.lower():
            raise PermissionError(
                "Access denied. Customers can only view their own tickets."
            )

        search_email = logged_in_email

    elif role in ("admin", "manager"):
        # Admin/Manager can search any customer
        search_email = customer_email or logged_in_email

    else:
        raise PermissionError("Unauthorized role.")

    tickets = TicketService.get_tickets_by_product(
        customer_email=search_email,
        product=product,
        offset=offset,
        limit=limit,
    )

    return [
        {
            "ticket_id": ticket.ticket_id,
            "customer_email": search_email,
            "product": ticket.product,
            "category": ticket.category,
            "status": ticket.status,
            "priority": ticket.priority,
            "channel": ticket.channel,
            "ticket_created_date": ticket.ticket_created_date,
        }
        for ticket in tickets
    ]