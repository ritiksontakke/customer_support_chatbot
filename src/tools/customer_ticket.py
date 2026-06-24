from src.config.database import engine
from langchain.tools import tool
from sqlalchemy import text


@tool("getTicketByCustomerEmail")
def get_tickets_by_customer_email(
customer_email: str,
offset: int = 0,
limit: int = 5
):
    """
    Retrieve the most recent support tickets for the authenticated customer.

    Use this tool when a customer asks:
    - Tell me about my recent tickets
    - Show my latest tickets
    - Show my support history
    - What support requests have I opened?

    This is a READ-ONLY tool.

    The tool searches the customer_support_tickets table using the
    authenticated customer's email address and returns the most
    recent tickets ordered by newest first.

    Returns up to 5 tickets by default.
    """

    query = text("""
        SELECT *
        FROM customer_support_tickets
        WHERE customer_email = :customer_email
        ORDER BY ticket_created_date DESC
        LIMIT :limit
        OFFSET :offset
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {
                "customer_email": customer_email,
                "limit": limit,
                "offset": offset
            }
        )

        tickets = result.mappings().all()
    print("EMAIL =", customer_email)
    print("ROWS =", len(tickets))

    return [dict(ticket) for ticket in tickets]