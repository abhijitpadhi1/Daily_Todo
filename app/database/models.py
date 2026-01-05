from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    UniqueConstraint,
    Index
)

from app.database.db import Base

class TaskTemplate(Base):
    """SQLAlchemy model for task templates."""
    __tablename__ = "task_templates"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class DailyTask(Base):
    """SQLAlchemy model for daily tasks."""
    __tablename__ = "daily_tasks"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("task_templates.id"), nullable=False)
    task_date = Column(Date, nullable=False)

    completed = Column(Boolean, nullable=False, default=False)
    completed_at = Column(DateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint("task_id", "task_date", name="uq_task_day"),
        Index("idx_task_date", "task_date"),
        Index("idx_task_id", "task_id"),
    )


class DaySummary(Base):
    """SQLAlchemy model for daily task summaries."""
    __tablename__ = "day_summary"

    date = Column(Date, primary_key=True)
    total_tasks = Column(Integer, nullable=False)
    completed_tasks = Column(Integer, nullable=False)
    completion_pct = Column(Float, nullable=False)


