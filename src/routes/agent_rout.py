from fastapi import APIRouter
from pydantic import BaseModel
from src.agents.supervisor_agent import SupervisorAgent
from langfuse.callback import CallbackHandler

router = APIRouter()

supervior = SupervisorAgent()

class QueryRequest(BaseModel):
    query : str
    email : str


@router.get("/")
def home():
    return{"messages" : "QueryRequest agent is running"}

@router.post("/supervisor_agent")
async def execute_agent(request: QueryRequest):
    handler = CallbackHandler()

    result = supervior.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""
                    User Email: {request.email}

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
        "response" : result["messages"][-1].content
    }
