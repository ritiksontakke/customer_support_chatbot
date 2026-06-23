import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.auth_handler import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post(
    "/login",
    include_in_schema=False
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")

    if (
        form_data.username != username
        or
        form_data.password != password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        {
            "sub": form_data.username
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }