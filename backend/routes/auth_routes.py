from fastapi import (
    APIRouter,
    HTTPException,
    Depends
)

from backend.schemas.user import (
    RegisterRequest,
    LoginRequest
)

from backend.services.auth_service import (
    register_user,
    login_user
)

from backend.auth.dependencies import (
    get_current_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(data: RegisterRequest):

    try:

        return register_user(
            data.name,
            data.email,
            data.password
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/login")
def login(data: LoginRequest):

    try:

        return login_user(
            data.email,
            data.password
        )

    except Exception as e:

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )


@router.get("/me")
def me(
    current_user=Depends(
        get_current_user
    )
):

    return current_user