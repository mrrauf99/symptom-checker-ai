from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.routes import router
from backend.routes.auth_routes import (
    router as auth_router
)
from backend.routes.session_routes import (
    router as session_router
)
from backend.routes.message_routes import (
    router as message_router
)
from backend.routes.chat_routes import (
    router as chat_router
)
from backend.routes.profile_routes import (
    router as profile_router
)
from backend.utils.logger import logger


app = FastAPI(
    title="Symptom Checker AI API",
    description=(
        "Healthcare Symptom Checker backend. "
        "Provides disease prediction, chat sessions, "
        "user authentication, and profile management."
    ),
    version="1.0.0"
)

origins = [
    "http://localhost:5173",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)
app.include_router(auth_router)
app.include_router(session_router)
app.include_router(message_router)
app.include_router(chat_router)
app.include_router(profile_router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(
    request: Request,
    exc: Exception
):
    logger.error(
        f"Unexpected exception on "
        f"{request.method} {request.url.path}: {exc}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        }
    )


@app.get(
    "/",
    summary="API root",
    description="Returns a simple message confirming the API is running.",
    tags=["Health"]
)
def root():

    return {
        "message": "Symptom Checker AI API Running"
    }
