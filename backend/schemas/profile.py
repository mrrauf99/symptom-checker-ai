from pydantic import BaseModel, Field
from typing import Optional


class UpdateProfileRequest(BaseModel):

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Full name of the user"
    )

    age: int | None = Field(
        default=None,
        ge=1,
        le=120,
        description="Age in years (1–120)"
    )

    gender: str | None = Field(
        default=None,
        description="Gender (optional)"
    )


class ProfileResponse(BaseModel):

    id: str
    name: str
    email: str
    age: Optional[int] = None
    gender: Optional[str] = None
