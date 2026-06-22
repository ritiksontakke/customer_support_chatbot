from langchain.tools import tool
from langchain.agents import create_agent
from src.utils import get_model
from src.tools.get_ticket_status import get_tickets_by_customer_email_and_status
from src.tools.customer_ticket import get_tickets_by_customer_email
from src.tools.ticket_by_channel import get_tickets_by_channel
from src.tools.ticket_details import get_ticket_details
from src.tools.tickets_by_product import get_tickets_by_product
from src.utils import get_system_prompt

@tool("readonlyagents")
def get_read_only_agent(query: str):
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
        tools=[
            get_tickets_by_customer_email_and_status, 
            get_tickets_by_customer_email, 
            get_tickets_by_channel,
            get_ticket_details,
            get_tickets_by_product,
            ],
        system_prompt=get_system_prompt("cutomer_chatbot"),
    )

    result = readonlyagent.invoke({"messages": [{"role" :"user", "content":query}]})
    return result["messages"][-1].content