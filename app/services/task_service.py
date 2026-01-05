from datetime import datetime
from sqlalchemy.orm import Session

from app.database.models import TaskTemplate, DailyTask, DaySummary
from app.services.date_service import get_logical_date, is_today
from app.services.daily_generator import ensure_day_exists


def get_today_tasks(db: Session) -> list[tuple[DailyTask, str]]:
    """
    Retrieve today's daily tasks along with their template names.

    :param db: Database session
    :type db: Session
    :return: List of tuples containing DailyTask and its template name
    :rtype: list[tuple[DailyTask, str]]
    """
    today = get_logical_date()

    return (
        db.query(DailyTask, TaskTemplate.name)
        .join(TaskTemplate, DailyTask.task_id == TaskTemplate.id)
        .filter(DailyTask.task_date == today)
        .all()
    )


def create_task_template(db: Session, name: str) -> TaskTemplate:
    """
    Create a new task template and ensure it appears today.

    :param db: Database session
    :type db: Session
    :param name: Name of the task template
    :type name: str
    :return: The created TaskTemplate object
    :rtype: TaskTemplate
    """
    name = name.strip()

    if not name:
        raise ValueError("Task name cannot be empty")

    exists = (
        db.query(TaskTemplate)
        .filter(TaskTemplate.name == name)
        .first()
    )
    if exists:
        raise ValueError("Task already exists")

    template = TaskTemplate(
        name=name,
        is_active=True
    )

    db.add(template)
    db.commit()
    db.refresh(template)

    # Ensure today's daily task exists immediately
    ensure_day_exists(db)

    return template


def toggle_task_template(db: Session, template_id: int) -> TaskTemplate:
    """
    Enable or disable a task template (future days only).

    :param db: Database session
    :type db: Session
    :param template_id: ID of the task template to toggle
    :type template_id: int
    :return: The updated TaskTemplate object
    :rtype: TaskTemplate
    """
    template = db.query(TaskTemplate).get(template_id)

    if not template:
        raise ValueError("Task not found")

    template.is_active = not template.is_active
    db.commit()

    return template


def complete_task(db: Session, daily_task_id: int) -> DailyTask:
    """
    Mark a daily task as completed (today only).

    :param db: Database session
    :type db: Session
    :param daily_task_id: ID of the daily task to complete
    :type daily_task_id: int
    :return: The updated DailyTask object
    :rtype: DailyTask
    """
    task = db.query(DailyTask).get(daily_task_id)

    if not task:
        raise ValueError("Task not found")

    if not is_today(task.task_date):
        raise PermissionError("Cannot modify past or future tasks")

    if task.completed:
        return task  # idempotent

    task.completed = True
    task.completed_at = datetime.utcnow()

    _update_day_summary(db, task.task_date)

    db.commit()
    return task


def _update_day_summary(db: Session, task_date):
    """
    Docstring for _update_day_summary
    
    :param db: Description
    :type db: Session
    :param task_date: Description
    :type task_date: date
    """
    summary = (
        db.query(DaySummary)
        .filter(DaySummary.date == task_date)
        .first()
    )

    if not summary:
        return

    completed = (
        db.query(DailyTask)
        .filter(
            DailyTask.task_date == task_date,
            DailyTask.completed == True
        )
        .count()
    )

    summary.completed_tasks = completed
    summary.completion_pct = (
        (completed / summary.total_tasks) * 100
        if summary.total_tasks > 0 else 0.0
    )

