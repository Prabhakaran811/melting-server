
from pydantic import BaseModel, Field

from app.schemas.user_schema import UserResponse


class LoginRequest(BaseModel):
    employee_id: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=128)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse
