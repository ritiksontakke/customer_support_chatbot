from sqlalchemy import text
from src.config.database import engine
from langchain.tools import tool,ToolRuntime
from src.schemas.schemas import UserContext

@tool("GetTicketsByProduct")
def get_tickets_by_product(
runtime : ToolRuntime[UserContext],
product: str,
# customer_email: str,
offset: int = 0,
limit: int = 5
):
    """
    Get customer support tickets for a specific product.

    Use this tool whenever a customer:
    - asks "Tell me the tickets I have raised for my cloud service"
    - asks "Show my web service tickets"
    - asks "What tickets have I raised for product X?"
    - asks about tickets related to a specific product

    This is a READ-ONLY tool.

    The tool searches customer ticket data stored in Supabase and
    returns tickets belonging to the authenticated customer that
    are associated with the requested product.

    Returns matching customer tickets.
    """
    customer_email = runtime.context.customer_email
    

    query = text("""
        SELECT *
        FROM customer_support_tickets
        WHERE customer_email = :customer_email
        AND product = :product
        ORDER BY ticket_created_date DESC
        LIMIT :limit
        OFFSET :offset
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {
                "customer_email": customer_email,
                "product": product,
                "limit": limit,
                "offset": offset
            }
        )

        tickets = result.mappings().all()

    return [dict(ticket) for ticket in tickets]