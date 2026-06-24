from fastapi import APIRouter, Depends, HTTPException, Query
from src.schemas.schemas import Role
from src.auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/role",
    tags=["Role"]
)

verified_users = {}

@router.post("/select")
async def select_role(
    role: Role = Query(...),
    current_user=Depends(get_current_user)
):
    if role.value != current_user["role"]:
        raise HTTPException(
            status_code=403,
            detail="Invalid role selected"
        )

    verified_users[current_user["user_id"]] = True

    return {
        "message": "Role verified"
    }