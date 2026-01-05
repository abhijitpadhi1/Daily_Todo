# import sys
# import subprocess
# import webbrowser
# import time

# from app.database.db import SessionLocal
# from app.database.init_db import init_db
# from app.services.daily_generator import ensure_day_exists


# def run_app():
#     """
#     Entry point for `daily-todo run`
#     """
#     # 0. Initialize database and ensure today's state
#     init_db()

#     # 1. Ensure daily state exists
#     db = SessionLocal()
#     try:
#         ensure_day_exists(db)
#     finally:
#         db.close()

#     # 2. Start FastAPI server
#     print("Starting Daily Todo server...")
#     server = subprocess.Popen(
#         ["uvicorn", "app.main:app"],
#         stdout=subprocess.DEVNULL,
#         stderr=subprocess.DEVNULL,
#     )

#     # 3. Give server a moment to start
#     time.sleep(1.5)

#     # 4. Open browser
#     try:
#         webbrowser.open("http://localhost:8000")
#     except Exception:
#         print("Server started. Open http://localhost:8000 manually.")

#     # 5. Wait for server to exit
#     try:
#         server.wait()
#     except KeyboardInterrupt:
#         print("\nShutting down server...")
#         server.terminate()


# def main():
#     if len(sys.argv) < 2:
#         print("Usage: todo run")
#         sys.exit(1)

#     command = sys.argv[1]

#     if command == "run":
#         run_app()
#     else:
#         print(f"Unknown command: {command}")
#         print("Available commands: run")


import os
import sys
import webbrowser
import time

from app.database.db import SessionLocal
from app.database.init_db import init_db
from app.services.daily_generator import ensure_day_exists


def run_app():
    # 1. Ensure DB schema exists
    init_db()

    # 2. Ensure daily state exists
    db = SessionLocal()
    try:
        ensure_day_exists(db)
    finally:
        db.close()

    print("Starting Daily Todo server...")

    # 3. Open browser AFTER short delay
    def open_browser():
        time.sleep(1.5)
        try:
            webbrowser.open("http://localhost:8000")
        except Exception:
            pass

    import threading
    threading.Thread(target=open_browser, daemon=True).start()

    # 4. REPLACE current process with uvicorn (BLOCKING)
    os.execvp(
        "uvicorn",
        ["uvicorn", "app.main:app"]
    )

def main():
    if len(sys.argv) < 2:
        print("Usage: todo run")
        sys.exit(1)

    if sys.argv[1] == "run":
        run_app()
    else:
        print(f"Unknown command: {sys.argv[1]}")
        print("Available commands: run")