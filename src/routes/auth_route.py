from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.schemas.schemas import SignupRequest
from src.services.user_service import UserService
from src.auth.auth_handler import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/signup")
async def signup(data: SignupRequest):

    return UserService.signup(
        customer_name=data.username,
        customer_email=data.email,
        password=data.password,
    )


@router.post("/login", include_in_schema=False)
async def login(
    data: OAuth2PasswordRequestForm = Depends(),
):

    user = UserService.login(data.username)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email",
        )

    if not UserService.verify_password(
        data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password",
        )

    access_token = create_access_token(
        {
            "customer_email": user.email,
            "customer_name": user.name,
            "role": user.role,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "customer_email": user.email,
        "customer_name": user.name, 
        "role": user.role,
    }