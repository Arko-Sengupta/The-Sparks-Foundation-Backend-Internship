from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class SignUpRequest(BaseModel):
    fullName:    str = Field(..., min_length=4)
    email:       EmailStr
    phone:       str = Field(..., min_length=10, max_length=10)
    pan:         str = Field(..., min_length=10, max_length=10)
    password:    str = Field(..., min_length=8)
    address:     Optional[str] = ""
    accountType: str = Field(..., pattern="^(Savings|Current)$")

class LoginRequest(BaseModel):
    email:    EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token:   str
    token_type:     str = "bearer"
    user_id:        str
    full_name:      str
    email:          str
    account_number: str

class UserUpdateRequest(BaseModel):
    fullName:      Optional[str] = None
    phone:         Optional[str] = None
    address:       Optional[str] = None
    accountNumber: Optional[str] = None
    password:      Optional[str] = None

class UserResponse(BaseModel):
    id:            str
    fullName:      str
    email:         str
    phone:         str
    address:       str
    accountNumber: str
    accountType:   str
    balance:       float