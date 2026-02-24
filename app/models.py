from sqlalchemy import String, Integer, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date # avoid type issues

from .db import Base

"""
Definie our tables
"""


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    term: Mapped[str | None] = mapped_column(String(100), nullable=True)

    assignments: Mapped[list["Assignment"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan", # delete all assignments if course deleted
    )


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)

    # store as text; enforce allowed values with a CHECK constraint
    status: Mapped[str] = mapped_column(String(10), nullable=False, default="todo")
    priority: Mapped[int | None] = mapped_column(Integer, nullable=True)

    course: Mapped[Course] = relationship(back_populates="assignments")

    # Table constraints
    __table_args__ = (
        CheckConstraint("status IN ('todo', 'done')", name="ck_assignment_status"),
        CheckConstraint(
            "priority IS NULL OR (priority >= 1 AND priority <= 3)",
            name="ck_assignment_priority",
        ),
    )