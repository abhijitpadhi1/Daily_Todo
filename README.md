# 🗓️ DailyTodo – A Local Daily Task Tracker <br> (FastAPI + SQLite)

## 📌 Overview

**DailyTodo** is a **local-first daily task tracking web application** designed to reset every day at **3:00 AM**.
It focuses on **discipline, streaks, and consistency**, not complex task management.

This project was built **end-to-end**, including:

* Backend
* Database design
* UI
* CLI tooling
* Cron automation
* Shell lifecycle management

The goal was not just to “make it work”, but to **make it correct, reliable, and maintainable**.

---

## ✨ Features

* 🏠 **Home Page**

  * Daily tasks
  * Progress bar with color + emoji feedback
  * Motivational messages based on completion percentage

* ✅ **Task Marking Page**

  * Mark today’s tasks only
  * Completion timestamp displayed
  * No access to past/future tasks

* ➕ **Task Creation Page**

  * Create reusable task templates
  * Tasks start tracking from the same day
  * Enable/disable tasks anytime

* 📊 **Dashboard**

  * Current streak
  * Best streak
  * Weekly completion summary
  * Task-wise consistency

* 🕒 **Daily Reset at 3:00 AM**

  * Implemented via cron
  * Safe, idempotent logic
  * Works even if system was off

* 💻 **CLI Command**

  ```bash
  todo run
  ```

* 🖥️ **Home Directory Launcher Script**

  * Activates virtual environment
  * Runs the app
  * Cleans up on Ctrl+C

---

## 🧱 Tech Stack

* **Backend:** FastAPI
* **Frontend:** Jinja2 (minimal UI, no JS)
* **Database:** SQLite + SQLAlchemy
* **Automation:** Cron (Linux)
* **CLI:** Python entry points
* **Environment:** Virtualenv
* **OS:** Linux (local-only app)

---

## 📂 Project Structure

```
DailyTodo/
├── app/
│   ├── main.py
│   ├── cli.py
│   ├── routes/
│   ├── services/
│   ├── database/
│   ├── templates/
│   └── static/
├── cron/
│   └── daily_reset.sh
├── setup.py
├── requirements.txt
├── venv/
└── README.md
```

---

## 🚀 How to Run

### 1️⃣ Clone the repository

```bash
git clone github.com/abhijitpadhi1/Daily_Todo
cd DailyTodo
```

### 2️⃣ Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies and CLI

```bash
pip install -r requirements.txt
pip install -e .
```

### 4️⃣ Run the app

```bash
todo run
```

Browser opens automatically at:

```
http://localhost:8000
```

---

## 🕒 Cron Setup (Daily Reset at 3:00 AM)

A cron job runs every day at **03:00 AM** to generate daily tasks.

Cron entry:

```cron
0 3 * * * /absolute/path/to/DailyTodo/cron/daily_reset.sh
```

The script:

* Activates venv
* Runs the daily generator
* Logs execution
* Is safe to run multiple times

---

## 🖥️ Home Directory Launcher Script

A wrapper script allows running the app from **anywhere**:

```bash
~/todo-app.sh
```

What it does:

* Activates the virtual environment
* Moves into the project directory
* Runs `todo run`
* Blocks correctly
* On `Ctrl+C`, deactivates the venv cleanly

This solves:

* Working directory issues
* Environment lifecycle issues
* Orphan process problems

---

## 🧠 Key Design Decisions

### ✅ Logical Day (3:00 AM Reset)

Instead of midnight, the “day” resets at 3 AM to better match real human routines.

### ✅ Idempotent Services

Daily task generation and summaries can run multiple times without duplication.

### ✅ Separation of Concerns

* DB models → persistence
* Services → business logic
* Routes → HTTP handling
* UI → presentation only

### ✅ Local-First Philosophy

No deployment, no cloud, no auth.
Designed for **personal productivity**, not scale.

---

## 🧪 Major Bugs & What I Learned

This project intentionally documents **real mistakes and fixes**, not just success.

### 🔴 Bug: Progress always showed `0 / 0`

**Cause:**
Summary table was not recomputed after task creation.

**Fix:**
Always derive summary from daily tasks, never treat it as source of truth.

📌 *Lesson:* Derived data must stay derived.

---

### 🔴 Bug: Task names missing on marking page

**Cause:**
Joined SQLAlchemy queries return tuples, not models.

**Fix:**
Explicit tuple unpacking in Jinja templates.

📌 *Lesson:* ORM joins change data shape — UI must respect that.

---

### 🔴 Bug: Cron failed silently

**Cause:**
Spaces in project path + heredoc shell execution.

**Fix:**
Use quoted Python execution with `-c`.

📌 *Lesson:* Cron environments are minimal and unforgiving.

---

### 🔴 Bug: CLI exited immediately

**Cause:**
CLI spawned uvicorn instead of replacing itself.

**Fix:**
Use `os.execvp()` so CLI becomes the server process.

📌 *Lesson:* Foreground processes matter in Unix systems.

---

### 🔴 Bug: App failed when launched from home directory

**Cause:**
Relative paths and wrong working directory.

**Fix:**

* Resolve paths using `__file__`
* `cd` into project directory in launcher script

📌 *Lesson:* Never rely on CWD in production-style apps.

---

## 🏁 Final Outcome

By the end of this project, I gained hands-on experience with:

* FastAPI internals
* SQLAlchemy lifecycle
* Cron reliability
* CLI tooling
* Unix process management
* Debugging real production-style issues
* Designing for correctness, not shortcuts

This project reflects **how software behaves in the real world**, not just in tutorials.

---

## 📌 Future Improvements (Optional)

* Weekly/monthly charts
* Export analytics (CSV)
* Desktop launcher
* Systemd user service
* Mobile-friendly UI

---

## 👤 Author

**Abhijit Padhi1**
Built as a learning-focused, engineering-first project.

---
