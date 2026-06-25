from sqlalchemy import text
from src.config.database import engine
from langchain.tools import tool , ToolRuntime
from src.schemas.schemas import UserContext

@tool("GetTicketStatus")
def get_tickets_by_customer_email_and_status(
runtime : ToolRuntime[UserContext],
status: str,
# customer_email: str,
offset: int = 0,
limit: int = 5
):
    # customer_email REMOVE | * config -> transfer data || agent to tools | agent to subagent 
    """
    Get the most recent support tickets for an authenticated customer filtered by ticket status.

    Use this tool whenever a customer:
    - asks about their closed tickets
    - asks about their open tickets
    - asks about their in-progress tickets
    - asks "Tell me about my recent closed tickets"
    - asks "Show my latest open tickets"
    - asks "What in-progress tickets do I have?"
    - asks "Tell me about my recent tickets which are closed/open/in-progress"

    This is a READ-ONLY tool.

    The tool searches customer ticket data stored in Supabase and returns
    the customer's most recent tickets matching the requested status.

    Returns up to 5 tickets ordered from newest to oldest.
    """
    customer_email = runtime.context.customer_email

    query = text("""
        SELECT *
        FROM customer_support_tickets
        WHERE customer_email = :customer_email
        AND status = :status
        ORDER BY ticket_created_date DESC
        LIMIT :limit
        OFFSET :offset
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {
                "customer_email": customer_email,
                "status": status,
                "limit": limit,
                "offset": offset
            }
        )

        tickets = result.mappings().all()

    return [dict(ticket) for ticket in tickets]