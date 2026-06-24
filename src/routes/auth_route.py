from passlib.context import CryptContext
import hashlib
from sqlalchemy import text
from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from src.schemas.schemas import SignupRequest
from src.config.database import engine
from passlib.context import CryptContext
from src.schemas.schemas import LoginRequest
from src.auth.auth_handler import create_access_token
router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

@router.post("/signup")
async def signup(data: SignupRequest):

    hashed_password = pwd_context.hash(
        data.password
    )

    query = """
    INSERT INTO users
    (username, email, password)
    VALUES
    (:username, :email, :password)
    """

    try:

        with engine.begin() as conn:

            conn.execute(
                text(query),
                {
                    "username": data.username,
                    "email": data.email,
                    "password": hashed_password
                }
            )

        return {
            "message": "User created successfully"
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.post("/login", include_in_schema=False)
async def login(
    data: OAuth2PasswordRequestForm = Depends()
):

    query = """
    SELECT *
    FROM customer_support_tickets
    WHERE customer_email = :customer_email
    """

    with engine.begin() as conn:
        user = conn.execute(
            text(query),
            {
                "customer_email": data.username
            }
        ).mappings().first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email"
        )

    # Plain password check
    if data.password != user["password"]:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    access_token = create_access_token(
        {
            "customer_email": user["customer_email"],
            "role": user["role"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "customer_email": user["customer_email"],
        "role": user["role"]
    }