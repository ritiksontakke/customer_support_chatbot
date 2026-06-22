from fastapi import FastAPI
from src.routes.agent_rout import router

app = FastAPI(
    title="coustmer chat bot"
)

app.include_router(router)
