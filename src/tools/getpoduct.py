from typing import Optional

from langchain.tools import tool, ToolRuntime
from src.schemas.schemas import UserContext
from src.services.ticket_service import TicketService


@tool("GetProduct")
def get_product(
    runtime: ToolRuntime[UserContext],
    product: Optional[str] = None,
    customer_email: Optional[str] = None,
    offset: int = 0,
    limit: int = 5,
):
    """
    Retrieve product-related ticket information for a customer.

    This is a **read-only** tool that returns product details associated with
    support tickets. It supports searching by product name (including partial
    or misspelled product names if supported by the backend search) and enforces
    role-based access control (RBAC).

    Role-Based Access Control (RBAC):
        - Customer:
            - Can retrieve only their own product/ticket information.
            - The logged-in customer's email is always used for the search.
            - If a different `customer_email` is provided, a PermissionError
              is raised.

        - Manager:
            - Can retrieve product information for any customer.
            - If `customer_email` is omitted, their own email is used.

        - Admin:
            - Has the same access as Manager.
            - Can retrieve product information for any customer.

    Args:
        runtime (ToolRuntime[UserContext]):
            Runtime context containing the authenticated user's information,
            including email address and role.

        product (Optional[str], optional):
            Product name to search for. Supports partial or approximate
            matches depending on the underlying search implementation.
            If omitted, returns products associated with the customer.

        customer_email (Optional[str], optional):
            Customer email whose product information should be retrieved.
            - Ignored for customers (their logged-in email is always used).
            - Supported for managers and admins.

        offset (int, optional):
            Number of records to skip for pagination.
            Defaults to 0.

        limit (int, optional):
            Maximum number of records to return.
            Defaults to 5.

    Returns:
        list[dict]:
            A list of dictionaries containing product-related ticket details,
            including:
                - ticket_id
                - customer_email
                - product
                - category
                - status
                - priority
                - channel
                - ticket_created_date

    Raises:
        PermissionError:
            If:
            - A customer attempts to access another customer's product
              information.
            - The authenticated user's role is not Customer, Manager,
              or Admin.

            Example error message:
            "Access denied. Customers are only authorized to view product
            information associated with their own account."

    Examples:
        Customer:
            >>> get_product(product="Laptop")
            Returns the logged-in customer's product tickets.

        Customer (Unauthorized):
            >>> get_product(customer_email="ritik@gmail.com")
            PermissionError:
            "Access denied. Customers are only authorized to view product
            information associated with their own account."

        Manager:
            >>> get_product(customer_email="ritik@gmail.com")
            Returns product tickets for ritik@gmail.com.

        Admin:
            >>> get_product(product="Mouse", customer_email="ritik@gmail.com")
            Returns matching product tickets for the specified customer.
    """

    logged_in_email = runtime.context.customer_email
    role = runtime.context.role.lower()

    # RBAC
    if role == "customer":
        # Customer cannot search another user's data
        if customer_email and customer_email.lower() != logged_in_email.lower():
            return {
                "success": False,
                "message": "Access denied. Customers are authorized to view only their own support tickets."
            }

        search_email = logged_in_email

    elif role in ("admin", "manager"):
        # Admin/Manager can search any customer
        search_email = customer_email or logged_in_email

    else:
        return {
            "success": False,
            "message": "Access denied. Your account does not have permission to access customer ticket information."
        }

    tickets = TicketService.get_products(
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