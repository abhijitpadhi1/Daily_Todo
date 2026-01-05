#!/bin/bash

PROJECT_DIR="/home/abhijit/Use Directory/Python/DailyTodo"
VENV_DIR="$PROJECT_DIR/venv"
PYTHON="$VENV_DIR/bin/python"

LOG_FILE="$PROJECT_DIR/cron/cron.log"

source "$VENV_DIR/bin/activate"

echo "===========================================" >> "$LOG_FILE"
echo "[$(date)] Running daily task generator" >> "$LOG_FILE"

"$PYTHON" -c "
from app.database.db import SessionLocal
from app.services.daily_generator import ensure_day_exists

db = SessionLocal()
try:
    ensure_day_exists(db)
finally:
    db.close()
" >> "$LOG_FILE" 2>&1

echo "[$(date)] Daily task generator finished" >> "$LOG_FILE"
echo "===========================================" >> "$LOG_FILE"