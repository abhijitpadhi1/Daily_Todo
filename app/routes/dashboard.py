from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.services.dashboard_service import get_dashboard_data
from app.routes.base import templates

router = APIRouter(prefix="/dashboard")

@router.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    """Display the dashboard with aggregated data."""
    data = get_dashboard_data(db)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "data": data
        }
    )
