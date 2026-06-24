from fastapi import APIRouter
from pydantic import BaseModel
from src.agents.supervisor_agent import SupervisorAgent
from langfuse.callback import CallbackHandler
from src.auth.oauth2 import get_current_user
from src.routes.role_route import verified_users
from fastapi import Depends,HTTPException
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
    if not verified_users.get(current_user["user_id"]):
        raise HTTPException(
            status_code=403,
            detail="Please select role first"
        )
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
