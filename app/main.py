from fastapi import FastAPI

from .db import engine, Base # db setup
from .routers import courses, assignments, analytics

"""
wire db, modelsm routers, and FastAPI into a runnable web server
"""
# Create tables on startup
Base.metadata.create_all(bind=engine)

# Create web app object with FastAPI (run with uvicorn)
app = FastAPI(title="Course Assignment Tracker")

# Add all defined endpoint in routers to app
app.include_router(courses.router)
app.include_router(assignments.router)
app.include_router(analytics.router)

# Show server status
@app.get("/health")
def health():
    return {"ok": True}