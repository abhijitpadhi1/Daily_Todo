from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.services.daily_generator import ensure_day_exists
from app.services.task_service import get_today_tasks
from app.services.dashboard_service import get_today_progress
from app.routes.base import templates

router = APIRouter()

@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    """Display today's tasks and progress on the home page."""
    # Safety net: ensure today exists
    ensure_day_exists(db)

    tasks, today = get_today_tasks(db)
    progress = get_today_progress(db)

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "tasks": tasks,
            "today": today,
            "progress": progress
        }
    )
