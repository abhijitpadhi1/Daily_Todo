from datetime import date
from sqlalchemy.orm import Session

from app.database.models import TaskTemplate, DailyTask, DaySummary
from app.services.date_service import get_logical_date

def ensure_day_exists(db: Session, target_date: date | None = None):
    """
    Ensures that daily tasks and summary exist for a logical day.
    Safe to call multiple times (idempotent).
    """
    if target_date is None:
        target_date = get_logical_date()

    _generate_daily_tasks(db, target_date)
    _ensure_day_summary(db, target_date)


def _generate_daily_tasks(db: Session, target_date: date):
    """
    Create daily task instances from active templates
    if they do not already exist.
    """
    templates = (
        db.query(TaskTemplate)
        .filter(TaskTemplate.is_active == True)
        .all()
    )

    for template in templates:
        exists = (
            db.query(DailyTask)
            .filter(
                DailyTask.task_id == template.id,
                DailyTask.task_date == target_date
            )
            .first()
        )

        if exists:
            continue

        daily_task = DailyTask(
            task_id=template.id,
            task_date=target_date,
            completed=False,
            completed_at=None
        )
        db.add(daily_task)

    db.commit()
    

def _ensure_day_summary(db: Session, target_date: date):
    """
    Ensure that a DaySummary entry exists for the target date.

    :param db: Database session
    :type db: Session
    :param target_date: The date for which to ensure the summary
    :type target_date: date
    """
    total_tasks = (
        db.query(DailyTask)
        .filter(DailyTask.task_date == target_date)
        .count()
    )

    completed_tasks = (
        db.query(DailyTask)
        .filter(
            DailyTask.task_date == target_date,
            DailyTask.completed == True
        )
        .count()
    )

    completion_pct = (
        (completed_tasks / total_tasks) * 100
        if total_tasks > 0 else 0.0
    )

    summary = (
        db.query(DaySummary)
        .filter(DaySummary.date == target_date)
        .first()
    )

    if summary:
        summary.total_tasks = total_tasks
        summary.completed_tasks = completed_tasks
        summary.completion_pct = completion_pct
        db.commit()
        return

    summary = DaySummary(
        date=target_date,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        completion_pct=completion_pct
    )

    db.add(summary)
    db.commit()

