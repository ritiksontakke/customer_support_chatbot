from src.utils import get_model
from langchain.agents import create_agent
from src.agents.readOnlyAgent import get_read_only_agent
from src.agents.writeAgent import get_write_only_agent
from src.utils import get_system_prompt
from src.schemas.schemas import UserContext
def SupervisorAgent():
    return create_agent(
        model=get_model(),
        tools=[get_read_only_agent,get_write_only_agent],
        context_schema=UserContext,
        system_prompt=get_system_prompt("cutomer_chatbot"),
)