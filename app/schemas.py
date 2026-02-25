"""
Defines i/o schemas that validate incoming JSON, convert JSON to python, enforce constraints, and convert back to json 
to send over HTTP.
"""

from datetime import date
from pydantic import BaseModel, Field


# ---------- Courses ----------
class CourseCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    term: str | None = Field(default=None, max_length=100)


class CourseOut(BaseModel):
    id: int
    name: str
    term: str | None

    class Config:
        from_attributes = True


# ---------- Assignments ----------
class AssignmentCreate(BaseModel):
    course_id: int
    title: str = Field(min_length=1, max_length=200)
    due_date: date  
    status: str = Field(default="todo", pattern="^(todo|done)$")
    priority: int | None = Field(default=None, ge=1, le=3)


class AssignmentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    due_date: date | None = None
    status: str | None = Field(default=None, pattern="^(todo|done)$")
    priority: int | None = Field(default=None, ge=1, le=3)


class AssignmentOut(BaseModel):
    id: int
    course_id: int
    title: str
    due_date: date
    status: str
    priority: int | None

    class Config:
        from_attributes = True