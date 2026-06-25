from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from dataclasses import dataclass

class Role(str, Enum):
    customer = "customer"
    admin = "admin"
    manager = "manager"

class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Role = Field(
        ...,
        examples=["customer", "manager", "admin"]
    )

class LoginRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Role = Field(
        ...,
        examples=["customer", "manager", "admin"]
    )

@dataclass
class UserContext:
    customer_email: str
    role : str