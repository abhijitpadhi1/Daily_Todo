from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo

# System-wide configuration
LOCAL_TIMEZONE = ZoneInfo("Asia/Kolkata")
DAY_RESET_HOUR = 3  # 3:00 AM


def get_now() -> datetime:
    """
    Returns current timezone-aware datetime.
    This is the ONLY place datetime.now() is allowed.
    """
    return datetime.now(tz=LOCAL_TIMEZONE)


def get_logical_date(now: datetime | None = None) -> date:
    """
    Returns the logical date based on the 3:00 AM rule.

    If time is before 03:00 AM, logical day = yesterday.
    Otherwise, logical day = today.
    """
    if now is None:
        now = get_now()

    if now.hour < DAY_RESET_HOUR:
        return (now - timedelta(days=1)).date()

    return now.date()


def is_today(task_date: date) -> bool:
    """
    Checks whether a given date is the current logical day.
    """
    return task_date == get_logical_date()
