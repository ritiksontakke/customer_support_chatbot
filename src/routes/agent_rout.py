from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.agents.supervisor_agent import SupervisorAgent
from langfuse.callback import CallbackHandler
from src.auth.oauth2 import get_current_user
import re

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
    customer_email = current_user["customer_email"]

    # Extract email from query if user typed one
    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    found_emails = re.findall(email_pattern, request.query)

    # If query contains another email, block it
    if found_emails:
        requested_email = found_emails[0]

        if requested_email.lower() != customer_email.lower():
            return {
                "query": request.query,
                "customer_email": customer_email,
                "response": (
                    "Sorry, I can't show information for another customer's account. "
                    "I can only access information associated with your authenticated account."
                )
            }

    handler = CallbackHandler()

    result = supervisor.invoke(
        {
            "messages": [
                {
                    "role": "system",
                    "content": f"""
Authenticated customer email: {customer_email}

IMPORTANT:
- Only access records for {customer_email}
- Ignore any other email mentioned by the user
- Never reveal another customer's information
"""
                },
                {
                    "role": "user",
                    "content": request.query
                }
            ],
            "customer_email": customer_email
        },
        config={
            "callbacks": [handler]
        }
    )

    return {
        "query": request.query,
        "customer_email": customer_email,
        "response": result["messages"][-1].content
    }