from fastapi import APIRouter
from pydantic import BaseModel
from src.agents.supervisor_agent import SupervisorAgent
from langfuse.callback import CallbackHandler
from src.auth.oauth2 import get_current_user
from fastapi import Depends
router = APIRouter()

supervior = SupervisorAgent()

class QueryRequest(BaseModel):
    query : str
    email : str


@router.get("/")
def home():
    return{"messages" : "QueryRequest agent is running"}

@router.post("/supervisor_agent")
async def execute_agent(request: QueryRequest , current_user = Depends(get_current_user)):
    handler = CallbackHandler()

    result = supervior.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""
                    Ticket ID: {request.email}
                    Query: {request.query}
                    """

                }
            ]
        },
        config={
            "callbacks": [handler]
        }
    )

    return{
        "query": request.query,
        "ticket_id" : request.email,
        "user" : current_user["username"],
        "response" : result["messages"][-1].content
    }
