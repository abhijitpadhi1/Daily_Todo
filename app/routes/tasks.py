from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.services.task_service import get_today_tasks, complete_task
from app.routes.base import templates

router = APIRouter(prefix="/tasks")

@router.get("/today")
def show_today_tasks(request: Request, db: Session = Depends(get_db)):
    """Display today's tasks for marking completion."""
    tasks, today = get_today_tasks(db)

    return templates.TemplateResponse(
        "mark.html",
        {
            "request": request,
            "tasks": tasks,
            "today": today
        }
    )


@router.post("/{task_id}/complete")
def mark_task_complete(task_id: int, db: Session = Depends(get_db)):
    """Mark a specific task as complete."""
    complete_task(db, task_id)
    return RedirectResponse("/tasks/today", status_code=303)
