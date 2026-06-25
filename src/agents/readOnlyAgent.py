from langchain.tools import tool,ToolRuntime
from langchain.agents import create_agent
from src.utils import get_model
from src.schemas.schemas import UserContext
from src.utils import get_system_prompt
from src.access_control.permissions import ROLE_TOOLS
from src.access_control.permission_manager import get_allowed_tools

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
    role = runtime.context.role
    tools = get_allowed_tools(role)
    if not tools:
        return f"Permission denied. No tools are available for role '{role}'."
    readonlyagent = create_agent(
        model=get_model(),
        tools=tools,
        context_schema=UserContext,
        system_prompt=get_system_prompt("cutomer_chatbot"),
    )

    result = readonlyagent.invoke({"messages": [{"role" :"user", "content":query}]} , context=runtime.context)
    return result["messages"][-1].content