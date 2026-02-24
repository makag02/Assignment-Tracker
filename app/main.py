from fastapi import FastAPI

from .db import engine, Base
from .routers import courses, assignments, analytics

# Create tables on startup (simple for a student project)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Course Assignment Tracker")

app.include_router(courses.router)
app.include_router(assignments.router)
app.include_router(analytics.router)


@app.get("/health")
def health():
    return {"ok": True}