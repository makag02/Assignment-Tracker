from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db import get_db
from .. import crud, schemas

router = APIRouter(tags=["analytics"])


@router.get("/upcoming", response_model=list[schemas.AssignmentOut])
def upcoming(days: int = Query(default=7, ge=1, le=365), db: Session = Depends(get_db)):
    return crud.upcoming_assignments(db, days)


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    return crud.summary(db)