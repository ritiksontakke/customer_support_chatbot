from sqlalchemy import text
from src.config.database import engine
from langchain.tools import tool

@tool("getTicketDetails")
def get_ticket_details(
ticket_id: str,
customer_email: str
):
    """
    Get complete details for a specific customer support ticket.

    Use this tool whenever a customer:
    - asks for ticket details
    - provides a ticket ID
    - asks "Tell me about ticket 101"
    - asks "Show details for ticket 101"
    - asks "What is the status of ticket 101?"

    This is a READ-ONLY tool.

    The tool searches customer ticket data stored in Supabase and
    returns complete information for the requested ticket.

    Only tickets belonging to the authenticated customer should be returned.

    Returns a single ticket record.
    """

    query = text("""
        SELECT *
        FROM customer_support_tickets
        WHERE ticket_id = :ticket_id
        AND customer_email = :customer_email
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {
                "ticket_id": ticket_id,
                "customer_email": customer_email
            }
        )

        ticket = result.mappings().first()

    return dict(ticket) if ticket else None
