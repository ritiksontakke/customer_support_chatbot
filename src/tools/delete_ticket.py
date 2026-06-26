from langchain.tools import tool, ToolRuntime

from src.schemas.schemas import UserContext
from src.services.ticket_service import TicketService


@tool("DeleteTicket")
def delete_ticket(
    runtime: ToolRuntime[UserContext],
    ticket_id: int | None = None,
    customer_email: str | None = None,
):
    """
    Delete customer support tickets.

    Description:
        Permanently deletes customer support ticket records.

    Permissions:
        Allowed Roles:
            - Admin

        Not Allowed:
            - Customer
            - Support Agent
            - Manager
            - Guest

    Access Rules:
        - Only an Admin can delete tickets.
        - Admin may delete any customer's ticket.
        - Admin may delete:
            • A single ticket using ticket_id.
            • All tickets belonging to a customer using customer_email.

    Args:
        ticket_id (int, optional):
            Ticket ID to delete.

        customer_email (str, optional):
            Customer email. Deletes all tickets belonging to that customer.

    Returns:
        dict:
            {
                "success": True,
                "deleted_records": 1,
                "message": "Ticket(s) deleted successfully."
            }

    Raises:
        PermissionError:
            If current user is not an Admin.

        ValueError:
            If no matching ticket exists.
    """

    if runtime.context.role.lower() != "admin":
        raise PermissionError(
            "Only Admin can delete tickets."
        )

    return TicketService.delete_ticket(
        ticket_id=ticket_id,
        customer_email=customer_email,
    )