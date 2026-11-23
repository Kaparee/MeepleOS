import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field

class UserBase(BaseModel):
    email: EmailStr
    nickname: str | None = None
    name: str | None = None
    surname: str | None = None
    phone_number: str | None = None

class UserCreate(UserBase):
    password: str = Field(min_length=6)

class UserLogin(BaseModel):
    credential: EmailStr | str
    password: str

class UserResponse(UserBase):
    id: uuid.UUID
    account_status: str
    user_role: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"