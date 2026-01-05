from datetime import timedelta
from sqlalchemy.orm import Session

from app.database.models import DailyTask, DaySummary, TaskTemplate
from app.services.date_service import get_logical_date


def get_today_progress(db: Session) -> dict:
    """
    Returns today's progress summary including completed tasks, total tasks, and completion percentage.

    :param db: Database session
    :type db: Session
    :return: Dictionary with keys 'completed', 'total', and 'percent'
    :rtype: dict
    """
    today = get_logical_date()

    summary = (
        db.query(DaySummary)
        .filter(DaySummary.date == today)
        .first()
    )

    if not summary or summary.total_tasks == 0:
        return {
            "completed": 0,
            "total": 0,
            "percent": 0.0
        }

    return {
        "completed": summary.completed_tasks,
        "total": summary.total_tasks,
        "percent": summary.completion_pct
    }


def get_current_streak(db: Session) -> int:
    """
    Calculates the current streak of days with 100% task completion up to today.

    :param db: Database session
    :type db: Session
    :return: Number of consecutive days with 100% completion
    :rtype: int
    """
    today = get_logical_date()
    streak = 0
    cursor = today

    while True:
        summary = (
            db.query(DaySummary)
            .filter(DaySummary.date == cursor)
            .first()
        )

        if not summary or summary.completion_pct < 100:
            break

        streak += 1
        cursor -= timedelta(days=1)

    return streak


def get_best_streak(db: Session) -> int:
    """
    Calculates the best streak of days with 100% task completion.

    :param db: Database session
    :type db: Session
    :return: Best number of consecutive days with 100% completion
    :rtype: int
    """
    summaries = (
        db.query(DaySummary)
        .order_by(DaySummary.date)
        .all()
    )

    best = 0
    current = 0
    last_date = None

    for s in summaries:
        if s.completion_pct == 100:
            if last_date and (s.date - last_date).days == 1:
                current += 1
            else:
                current = 1
            best = max(best, current)
        else:
            current = 0

        last_date = s.date

    return best


def get_weekly_summary(db: Session, days: int = 7) -> list[dict]:
    """
    Retrieves the completion percentage for each day in the past week.

    :param db: Database session
    :type db: Session
    :param days: Number of days to retrieve summary for (default is 7)
    :type days: int
    :return: List of dictionaries with 'date' and 'percent' keys
    :rtype: list[dict]
    """
    today = get_logical_date()
    start = today - timedelta(days=days - 1)

    summaries = (
        db.query(DaySummary)
        .filter(DaySummary.date >= start)
        .order_by(DaySummary.date)
        .all()
    )

    return [
        {
            "date": s.date,
            "percent": s.completion_pct
        }
        for s in summaries
    ]


def get_task_consistency(db: Session) -> list[dict]:
    """
    Calculates the consistency percentage for each task across all days.

    :param db: Database session
    :type db: Session
    :return: List of dictionaries with 'task' and 'percent' keys
    :rtype: list[dict]
    """
    results = []

    tasks = db.query(TaskTemplate).all()

    for task in tasks:
        total_days = (
            db.query(DailyTask)
            .filter(DailyTask.task_id == task.id)
            .count()
        )

        if total_days == 0:
            continue

        completed_days = (
            db.query(DailyTask)
            .filter(
                DailyTask.task_id == task.id,
                DailyTask.completed == True
            )
            .count()
        )

        percent = (completed_days / total_days) * 100

        results.append({
            "task": task.name,
            "percent": round(percent, 1)
        })

    return results


def get_dashboard_data(db: Session) -> dict:
    """
    Aggregates all dashboard data into a single dictionary.

    :param db: Database session
    :type db: Session
    :return: Dictionary containing all dashboard metrics
    :rtype: dict
    """
    return {
        "current_streak": get_current_streak(db),
        "best_streak": get_best_streak(db),
        "weekly": get_weekly_summary(db),
        "task_consistency": get_task_consistency(db)
    }

