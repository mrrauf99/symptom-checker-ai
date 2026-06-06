from fastapi import FastAPI

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


app = FastAPI(
    title="Symptom Checker AI API"
)

app.include_router(router)
app.include_router(auth_router)
app.include_router(session_router)
app.include_router(message_router)
app.include_router(chat_router)

@app.get("/")
def root():

    return {
        "message": "Symptom Checker AI API Running"
    }