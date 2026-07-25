from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.agents.supervisor_agent import SupervisorAgent
from langfuse.callback import CallbackHandler
from src.auth.oauth2 import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.schemas import UserContext
import json
from fastapi.responses import StreamingResponse

router = APIRouter()

supervisor = SupervisorAgent()


class QueryRequest(BaseModel):
    query: str
    thread_id: str


@router.get("/")
def home():
    return {"message": "Agent is running"}



@router.post("/supervisor_agent")
async def execute_agent(
    request: QueryRequest,
    current_user=Depends(get_current_user)
):
    handler = CallbackHandler()

    try:
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
                customer_email=current_user["customer_email"],
                role=current_user["role"]
            ),
            config={
                "configurable": {"thread_id": request.thread_id},
                "callbacks": [handler]
            },
        
        )

        return {
            "query": request.query,
            "customer_email": current_user["customer_email"],
            "role": current_user["role"],
            "response": result["messages"][-1].content
        }

    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@router.post("/query")
async def query(
    request: QueryRequest,
    current_user=Depends(get_current_user),
):

    async def event_generator():
        result = await supervisor.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": request.query,
                    }
                ]
            },
            config={
                "configurable": {
                    "thread_id": request.thread_id
                }
            },
            context=UserContext(
                customer_email=current_user["customer_email"],
                role=current_user["role"],
            ),
        )

        messages = result.get("messages", [])
        print(messages)
        print(result)


        if messages:
            ai_message = messages[-1]
            yield ai_message.content
        else:
            yield "No response generated."

    return StreamingResponse(
        event_generator(),
        media_type="text/plain",
    )