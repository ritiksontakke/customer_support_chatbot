from src.utils import get_model
from langchain.agents import create_agent
from src.agents.readOnlyAgent import get_read_only_agent
from src.utils import get_system_prompt

def SupervisorAgent():
    return create_agent(
        model=get_model(),
        tools=[get_read_only_agent],
        system_prompt=get_system_prompt("cutomer_chatbot"),
)