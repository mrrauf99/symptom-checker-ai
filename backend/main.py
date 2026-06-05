from fastapi import FastAPI

from backend.api.routes import router

app = FastAPI(
    title="Healthcare Symptom Checker"
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Healthcare API Running"
    }