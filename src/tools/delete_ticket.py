from langchain.tools import tool, ToolRuntime

from src.schemas.schemas import UserContext
from src.services.ticket_service import TicketService

@tool("deleteTicket")
def delete_ticket(
    runtime: ToolRuntime[UserContext],
    ticket_id: int | None = None,
    customer_email: str | None = None,
):
    """
    Delete a customer support ticket.

    This tool performs a DELETE operation.

    Always use this tool whenever the user requests to:
    - Delete ticket 2
    - Delete support ticket 2
    - Remove ticket 2
    - Delete ticket ID 2
    - Delete the ticket for john@gmail.com
    - Remove the support ticket for john@gmail.com
    - Permanently delete a ticket

    Search Criteria
    ---------------
    - ticket_id
    - customer_email

    At least one of the above parameters must be provided.

    Authorization
    -------------
    - Admin:
        Authorized to delete any support ticket.

    - Manager:
        Not authorized to delete tickets.

    - Customer:
        Not authorized to delete tickets.

    If the authenticated user's role is not "admin",
    raise:

    PermissionError(
        "Access denied. Only administrators are authorized to delete support tickets."
    )

    Never answer a delete request directly.
    Always invoke this tool first.
    """
    print("=== deleteTicket CALLED ===")

    user_role = str(runtime.context.role).strip().lower()

    # Only Admin can delete tickets
    if user_role != "admin":
        raise PermissionError(
            "Access denied. Only administrators are authorized to delete support tickets."
        )

    if ticket_id is None and customer_email is None:
        raise ValueError(
            "Either 'ticket_id' or 'customer_email' must be provided."
        )

    return TicketService.delete_ticket(
        ticket_id=ticket_id,
        customer_email=customer_email,
    )