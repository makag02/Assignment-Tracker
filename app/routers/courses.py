from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..db import get_db
from .. import crud, schemas

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("", response_model=schemas.CourseOut, status_code=201)
def create_course(data: schemas.CourseCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_course(db, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="course_name_already_exists")


@router.get("", response_model=list[schemas.CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return crud.list_courses(db)


@router.get("/{course_id}", response_model=schemas.CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    c = crud.get_course(db, course_id)
    if c is None:
        raise HTTPException(status_code=404, detail="course_not_found")
    return c