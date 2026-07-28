from src.services.ticket_service import TicketService
from langchain.tools import tool, ToolRuntime
from src.schemas.schemas import UserContext

@tool("create_ticket_by_customer")
def create_ticket_by_customer(
    product: str,
    issue_description: str,
    runtime: ToolRuntime[UserContext],
):
    """
    Create a new customer support ticket.

    IMPORTANT:

    If the customer explicitly asks to create, raise, log, or open a support ticket,
    AND the product and issue can be identified from the user's message,
    CALL THIS TOOL IMMEDIATELY.

    Do NOT ask for:
    - Serial number
    - Purchase date
    - Warranty information
    - Contact details
    - Device model
    - Troubleshooting steps

    These details are optional and can be collected later by the support team.

    A product name and a short issue description are sufficient to create a ticket.

    This tool is available only for authenticated users with the Customer role.

    When to use:
    - The customer asks to create a support ticket.
    - The customer asks to raise a complaint.
    - The customer asks to log an issue.
    - The customer reports a problem with a product or service and expects support.

    If the product and issue are already present in the user's request,
    DO NOT ask follow-up questions.
    Call this tool immediately.

    Information to extract:

    product:
    Extract the product or service exactly as mentioned by the customer.

    Examples:
    - Dell Laptop
    - Laptop
    - Vivo Mobile
    - Broadband
    - Printer

    issue_description:
    Extract a short description of the issue using the customer's own words.

    Examples:
    - Display is black
    - Screen not working
    - Internet disconnecting frequently
    - Printer not printing

    Only ask a follow-up question if the product cannot be identified.

    Business Rules:
    - Only authenticated customers can create support tickets.
    - Customer name and email are automatically obtained from the authenticated session.
    - Do not ask the customer for their name or email.
    - Only one active ticket is allowed for the same customer and product.
    - If an active ticket exists, return that ticket instead of creating a new one.
    - New tickets always have status "Open".

    Returns:

    Success:
    {
        "success": True,
        "ticket_id": 101,
        "status": "Open",
        "message": "Ticket created successfully."
    }

    Failure:
    {
        "success": False,
        "ticket_id": 101,
        "message": "An active ticket already exists for this product."
    }
    """
    print("create tickets")
    user = runtime.context

    return TicketService.create_ticket_by_customer(
        customer_name=user.customer_name,
        customer_email=user.customer_email,
        product=product,
        issue_description=issue_description,
    )