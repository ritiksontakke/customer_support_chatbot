from fastapi import FastAPI
from src.routes.agent_rout import router
from src.routes.auth_route import router as auth_router

app = FastAPI(
    title="coustmer chat bot"
)

app.include_router(auth_router)
# app.include_router(role_router)
app.include_router(router)

#uvicorn src.main:app --reload