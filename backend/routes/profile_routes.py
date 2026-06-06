from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from backend.auth.dependencies import (
    get_current_user
)

from backend.schemas.profile import (
    UpdateProfileRequest
)

from backend.services.profile_service import (
    get_profile,
    update_profile
)

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


@router.get(
    "/",
    summary="Get user profile",
    description=(
        "Returns the authenticated user's profile including "
        "name, email, age, and gender."
    )
)
def profile(
    current_user=Depends(
        get_current_user
    )
):

    profile_data = get_profile(
        current_user["user_id"]
    )

    if not profile_data:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return profile_data


@router.put(
    "/",
    summary="Update user profile",
    description=(
        "Updates the authenticated user's profile fields. "
        "Name is required; age and gender are optional."
    )
)
def update_user_profile(
    data: UpdateProfileRequest,
    current_user=Depends(
        get_current_user
    )
):

    return update_profile(
        current_user["user_id"],
        data
    )
