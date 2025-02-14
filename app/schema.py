from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

# User Role Enum
class UserRole(str, Enum):
    admin = "admin"
    doctor = "doctor"
    nurse = "nurse"
    receptionist = "receptionist"
    pharmacist = "pharmacist"
    patient = "patient"

# User Registration Schema
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole

# User Response Schema (hides password)
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True  # Enable ORM mode

# Token Schema for Authentication
class Token(BaseModel):
    access_token: str
    token_type: str
