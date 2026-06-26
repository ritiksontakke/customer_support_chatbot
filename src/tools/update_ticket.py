from langchain.tools import tool, ToolRuntime

from src.schemas.schemas import UserContext
from src.services.ticket_service import TicketService


@tool("updateTicket")
def update_ticket(
    runtime: ToolRuntime[UserContext],
    updates: dict,
    ticket_id: int | None = None,
    customer_email: str | None = None,
):
    """
    Update an existing customer support ticket.

    Description:
        This tool allows an administrator to update one or more
        fields of a customer support ticket.

        The ticket can be identified using either:
        - ticket_id
        - customer_email

        Only the fields present in the updates dictionary
        will be modified.

    Permissions:
        Allowed Roles:
            - Admin

        Not Allowed:
            - Customer
            - Manager
            - Support Agent
            - Guest

    Args:
        ticket_id:
            Ticket ID to update.

        customer_email:
            Customer email whose ticket should be updated.

        updates:
            Dictionary containing fields to update.

            Example:
            {
                "status": "Open",
                "priority": "High",
                "resolution_notes": "Issue resolved"
            }

    Returns:
        Updated ticket information.
    """

    if runtime.context.role.lower() != "admin":
        raise PermissionError(
            "Only Admin can update tickets."
        )

    if ticket_id is None and customer_email is None:
        raise ValueError(
            "Provide ticket_id or customer_email."
        )

    return TicketService.update_ticket(
        ticket_id=ticket_id,
        customer_email=customer_email,
        updates=updates,
    )