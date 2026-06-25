from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.agents.supervisor_agent import SupervisorAgent
from langfuse.callback import CallbackHandler
from src.auth.oauth2 import get_current_user
import re
from src.schemas.schemas import UserContext
router = APIRouter()

supervisor = SupervisorAgent()


class QueryRequest(BaseModel):
    query: str


@router.get("/")
def home():
    return {"message": "Agent is running"}


@router.post("/supervisor_agent")
async def execute_agent(
    request: QueryRequest,
    current_user=Depends(get_current_user)
):

    handler = CallbackHandler()

    result = supervisor.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": request.query
                }
            ],
        },
        context=UserContext(
            customer_email=current_user["customer_email"]
        ),

        config={
            "callbacks": [handler]
        }
    )

    return {
        "query": request.query,
        "customer_email": current_user["customer_email"],
        "response": result["messages"][-1].content
    }