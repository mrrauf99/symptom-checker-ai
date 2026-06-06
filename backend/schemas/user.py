from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Full name of the user"
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=6,
        max_length=50,
        description="Password (minimum 6 characters)"
    )


class LoginRequest(BaseModel):
    email: EmailStr

    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
