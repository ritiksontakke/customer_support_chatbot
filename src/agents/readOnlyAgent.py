from langchain.tools import tool,ToolRuntime
from langchain.agents import create_agent
from src.utils import get_model
from src.tools.get_ticket_status import get_tickets_by_customer_email_and_status
from src.tools.customer_ticket import get_tickets_by_customer_email
from src.tools.ticket_by_channel import get_tickets_by_channel
from src.tools.ticket_details import get_ticket_details
from src.tools.tickets_by_product import get_tickets_by_product
from src.schemas.schemas import UserContext
from src.utils import get_system_prompt
from src.auth.permissions import ROLE_TOOLS
from src.tools.get_ticket_status import (
    get_tickets_by_customer_email_and_status
)
from src.tools.customer_ticket import (
    get_tickets_by_customer_email
)
from src.tools.ticket_by_channel import (
    get_tickets_by_channel
)
from src.tools.ticket_details import (
    get_ticket_details
)
from src.tools.tickets_by_product import (
    get_tickets_by_product
)

ALL_TOOLS = {
    "get_tickets_by_customer_email_and_status":
        get_tickets_by_customer_email_and_status,

    "get_tickets_by_customer_email":
        get_tickets_by_customer_email,

    "get_ticket_details":
        get_ticket_details,

    "get_tickets_by_channel":
        get_tickets_by_channel,

    "get_tickets_by_product":
        get_tickets_by_product,
}

# allowed_tool_names = ROLE_TOOLS["customer"]

# tools = [
#     ALL_TOOLS[name]
#     for name in allowed_tool_names
# ]


@tool("readonlyagents")
def get_read_only_agent(query: str , runtime: ToolRuntime[UserContext]):
    """
    Handle customer support information requests by delegating them
    to a specialized ReadOnly Agent.

    Use this tool when a customer wants to:
    - view recent tickets
    - check ticket status
    - view ticket details
    - view tickets by channel
    - view tickets by product

    The agent determines which read-only tool should be used and
    returns the relevant customer ticket information.

    Args:
        query (str): The customer's support request.

    Returns:
        str: The ReadOnly Agent's response containing customer
        ticket information retrieved from Supabase.
    """
    readonlyagent = create_agent(
        model=get_model(),
        tools=list(ALL_TOOLS.values()),
        context_schema=UserContext,
        system_prompt=get_system_prompt("cutomer_chatbot"),
    )

    result = readonlyagent.invoke({"messages": [{"role" :"user", "content":query}]} , context=runtime.context)
    return result["messages"][-1].content