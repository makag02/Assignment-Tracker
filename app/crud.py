from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from . import models, schemas
"""
Create, read, update, delete rows in DB and run queries in sql
"""

# ----- Courses -----
def create_course(db: Session, data: schemas.CourseCreate) -> models.Course:
    course = models.Course(name=data.name, term=data.term)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def list_courses(db: Session) -> list[models.Course]:
    return list(db.scalars(select(models.Course).order_by(models.Course.name)))


def get_course(db: Session, course_id: int) -> models.Course | None:
    return db.get(models.Course, course_id)


# ----- Assignments -----
def create_assignment(db: Session, data: schemas.AssignmentCreate) -> models.Assignment:
    # Ensure course exists
    course = db.get(models.Course, data.course_id)
    if course is None:
        raise ValueError("course_not_found")

    a = models.Assignment(
        course_id=data.course_id,
        title=data.title,
        due_date=data.due_date,
        status=data.status,
        priority=data.priority,
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


def list_assignments(
    db: Session,
    course_id: int | None = None,
    status: str | None = None,
    due_before: date | None = None,
    due_after: date | None = None,
) -> list[models.Assignment]:
    stmt = select(models.Assignment)

    if course_id is not None:
        stmt = stmt.where(models.Assignment.course_id == course_id)
    if status is not None:
        stmt = stmt.where(models.Assignment.status == status)
    if due_before is not None:
        stmt = stmt.where(models.Assignment.due_date <= due_before)
    if due_after is not None:
        stmt = stmt.where(models.Assignment.due_date >= due_after)

    stmt = stmt.order_by(models.Assignment.due_date.asc(), models.Assignment.id.asc())
    return list(db.scalars(stmt))


def update_assignment(
    db: Session, assignment_id: int, patch: schemas.AssignmentUpdate
) -> models.Assignment | None:
    a = db.get(models.Assignment, assignment_id)
    if a is None:
        return None

    if patch.title is not None:
        a.title = patch.title
    if patch.due_date is not None:
        a.due_date = patch.due_date
    if patch.status is not None:
        a.status = patch.status
    # priority: allow explicit nulling by sending {"priority": null}
    if patch.priority is not None or patch.priority is None:
        # only change if field was provided; Pydantic v2 provides model_fields_set
        if "priority" in patch.model_fields_set:
            a.priority = patch.priority

    db.commit()
    db.refresh(a)
    return a


def delete_assignment(db: Session, assignment_id: int) -> bool:
    a = db.get(models.Assignment, assignment_id)
    if a is None:
        return False
    db.delete(a)
    db.commit()
    return True


# ----- Smart queries -----
def upcoming_assignments(db: Session, days: int) -> list[models.Assignment]:
    today = date.today()
    end = today + timedelta(days=days)
    stmt = (
        select(models.Assignment)
        .where(models.Assignment.status == "todo")
        .where(models.Assignment.due_date >= today)
        .where(models.Assignment.due_date <= end)
        .order_by(models.Assignment.due_date.asc(), models.Assignment.id.asc())
    )
    return list(db.scalars(stmt))


def summary(db: Session) -> dict:
    today = date.today()

    total = db.scalar(select(func.count(models.Assignment.id))) or 0
    done = db.scalar(
        select(func.count(models.Assignment.id)).where(models.Assignment.status == "done")
    ) or 0
    todo = db.scalar(
        select(func.count(models.Assignment.id)).where(models.Assignment.status == "todo")
    ) or 0
    overdue = db.scalar(
        select(func.count(models.Assignment.id))
        .where(models.Assignment.status == "todo")
        .where(models.Assignment.due_date < today)
    ) or 0

    completion_rate = (done / total) if total else 0.0

    return {
        "total_assignments": total,
        "completed": done,
        "todo": todo,
        "overdue": overdue,
        "completion_rate": completion_rate,
        "today": today,
    }