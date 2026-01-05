from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.services.task_service import create_task_template, toggle_task_template
from app.database.models import TaskTemplate
from app.routes.base import templates

router = APIRouter(prefix="/create")

@router.get("/")
def show_create_page(request: Request, db: Session = Depends(get_db)):
    """Display the task creation page with existing templates."""
    templates_list = db.query(TaskTemplate).all()

    return templates.TemplateResponse(
        "create.html",
        {
            "request": request,
            "templates": templates_list
        }
    )


@router.post("/add")
def add_task(name: str = Form(...), db: Session = Depends(get_db)):
    """Add a new task template."""
    create_task_template(db, name)
    return RedirectResponse("/create", status_code=303)


@router.post("/{template_id}/toggle")
def toggle_task(template_id: int, db: Session = Depends(get_db)):
    """Toggle the active status of a task template."""
    toggle_task_template(db, template_id)
    return RedirectResponse("/create", status_code=303)
