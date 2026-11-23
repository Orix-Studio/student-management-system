# Student Management System

A small Python + MySQL app for registering and finding students.
Built step by step in the Python/Database 2 course.

## How to run

1. Start MySQL (`docker start ga-mysql`).
2. Create a virtual environment and install the packages:
   ```
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # Mac / Linux
   pip install -r requirements.txt
   ```
3. Copy `.env` to `.env` and fill in your password.
4. Run: `python app.py`

## Files

| File | Job |
|---|---|
| app.py | The main program: menu, input() and print() |
| student_repo.py | All the SQL for students (Lecture 2) |
| db.py | get_connection(): opens a connection using .env |
| .env | Database user and password. Private, never on GitHub |
| setup.sql | Builds the sms database and the sms_app user |
