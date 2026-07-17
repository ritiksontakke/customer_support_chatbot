from src.utils import get_model
from langchain.agents import create_agent
from src.agents.readOnlyAgent import get_read_only_agent
from src.agents.writeAgent import get_write_only_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from src.utils import get_system_prompt
from src.schemas.schemas import UserContext
from src.memory.store import store
def SupervisorAgent():
    return create_agent(
        model=get_model(),
        store=store,
        tools=[get_read_only_agent,get_write_only_agent],
        middleware=[
            ModelCallLimitMiddleware(
            thread_limit=10,
            run_limit=5,
        ),
    ],
        context_schema=UserContext,
        system_prompt=get_system_prompt("cutomer_chatbot"),
)