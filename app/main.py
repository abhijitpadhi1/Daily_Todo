from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database.init_db import init_db
from app.routes import home, tasks, create, dashboard

app = FastAPI(title="Daily Todo")

# --- Include Routers ---
app.include_router(home.router)
app.include_router(tasks.router)
app.include_router(create.router)
app.include_router(dashboard.router)

# --- Startup Hook ---
@app.on_event("startup")
def startup_event():
    init_db()

# --- Static Files ---

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# --- Health Check ---
@app.get("/")
def health_check():
    return {"status": "ok"}
