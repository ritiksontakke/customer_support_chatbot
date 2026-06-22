from sqlalchemy import text
from src.config.database import engine
from langchain.tools import tool

@tool("GetTicketsByChannel")
def get_tickets_by_channel(
channel: str,
customer_email: str,
offset: int = 0,
limit: int = 5
):
    """
    Get customer support tickets raised through a specific channel.

    Use this tool whenever a customer:
    - asks "Tell me the tickets I raised from my phone"
    - asks "Show my mobile tickets"
    - asks "Show tickets raised through Web Portal"
    - asks about tickets created through a specific channel

    This is a READ-ONLY tool.

    The tool searches customer ticket data stored in Supabase and
    returns tickets belonging to the authenticated customer that
    were raised through the requested channel.

    Returns the most recent matching tickets.
    """

    query = text("""
        SELECT *
        FROM customer_support_tickets
        WHERE customer_email = :customer_email
        AND channel = :channel
        ORDER BY ticket_created_date DESC
        LIMIT :limit
        OFFSET :offset
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {
                "customer_email": customer_email,
                "channel": channel,
                "limit": limit,
                "offset": offset
            }
        )

        tickets = result.mappings().all()
        print(tickets)

    return [dict(ticket) for ticket in tickets]
