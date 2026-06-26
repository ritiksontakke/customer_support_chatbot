import hashlib
from sqlalchemy import text
from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from src.schemas.schemas import SignupRequest
from src.config.database import engine
from src.services.ticket_service import TicketService
from src.schemas.schemas import LoginRequest
from src.auth.auth_handler import create_access_token
from passlib.context import CryptContext

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/signup")
async def signup(data: SignupRequest):

    try:

        return TicketService.signup(
            customer_name=data.username,
            customer_email=data.email,
            issue_description=data.issue_description,
            product = data.product,
            password=data.password,
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

  
@router.post("/login", include_in_schema=False)
async def login(
    data: OAuth2PasswordRequestForm = Depends(),
):

    user = TicketService.login(data.username)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email",
        )

    if not TicketService.verify_password(
        data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password",
        )

    access_token = create_access_token(
        {
            "customer_email": user.customer_email,
            "role": user.role,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "customer_email": user.customer_email,
        "role": user.role,
    }