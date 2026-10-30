from fastapi import FastAPI

from app.routers.students import router as students_router

app = FastAPI(
    title="Student API",
    description="A simple API for managing students.",
    version="1.0.0",
)

app.include_router(students_router, prefix="/api/v1")


@app.get("/", tags=["health"])
def read_root() -> dict[str, str]:
    return {"message": "Student API is running"}
