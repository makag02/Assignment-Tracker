from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db import get_db
from .. import crud, schemas

router = APIRouter(prefix="/assignments", tags=["assignments"])


@router.post("", response_model=schemas.AssignmentOut, status_code=201)
def create_assignment(data: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_assignment(db, data)
    except ValueError as e:
        if str(e) == "course_not_found":
            raise HTTPException(status_code=404, detail="course_not_found")
        raise


@router.get("", response_model=list[schemas.AssignmentOut])
def list_assignments(
    course_id: int | None = None,
    status: str | None = Query(default=None, pattern="^(todo|done)$"),
    due_before: date | None = None,
    due_after: date | None = None,
    db: Session = Depends(get_db),
):
    return crud.list_assignments(
        db, course_id=course_id, status=status, due_before=due_before, due_after=due_after
    )


@router.patch("/{assignment_id}", response_model=schemas.AssignmentOut)
def update_assignment(
    assignment_id: int, patch: schemas.AssignmentUpdate, db: Session = Depends(get_db)
):
    a = crud.update_assignment(db, assignment_id, patch)
    if a is None:
        raise HTTPException(status_code=404, detail="assignment_not_found")
    return a


@router.delete("/{assignment_id}", status_code=204)
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_assignment(db, assignment_id)
    if not ok:
        raise HTTPException(status_code=404, detail="assignment_not_found")