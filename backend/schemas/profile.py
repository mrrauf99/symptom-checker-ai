from pydantic import BaseModel, Field
from typing import Optional


class UpdateProfileRequest(BaseModel):

    name: str = Field(
        min_length=3,
        max_length=100
    )

    age: Optional[int] = None

    gender: Optional[str] = None


class ProfileResponse(BaseModel):

    id: str
    name: str
    email: str
    age: Optional[int] = None
    gender: Optional[str] = None