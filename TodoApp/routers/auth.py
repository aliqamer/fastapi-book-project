from fastapi import APIRouter
from pydantic import BaseModel
from models import Users

router = APIRouter()

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str = "user"  # Default role is set to "user"

@router.post("/auth")
async def create_user(create_user_request: CreateUserRequest):
    # Here you would typically hash the password and save the user to the database  
    # For now, we'll just return the user data as a response
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=create_user_request.password,  # In a real app, hash the password
        role=create_user_request.role,
        is_active=True  # Default to active
    )
    
    return create_user_model
    