# Catch-up guide: from zero to ready for Lecture 2

Do these steps in order. When you finish part F, you are exactly where Lecture 2 starts.

---

## A. Install the programs (one time only)

| Program | Why | Where to get it |
|---|---|---|
| Python 3.12+ | Runs app.py | https://www.python.org/downloads/ (Windows: tick **"Add python.exe to PATH"**) |
| Git | Saves versions of your code | https://git-scm.com/downloads |
| Docker Desktop | Runs MySQL in a container called `ga-mysql` | https://www.docker.com/products/docker-desktop/ |
| PyCharm (or VS Code) | Your editor | https://www.jetbrains.com/pycharm/ |
| DataGrip | Runs SQL in MySQL | https://www.jetbrains.com/datagrip/ (free with a student licence) |
| GitHub account | Stores your repository online | https://github.com/signup |

Check in a terminal:
```
python --version
git --version
docker --version
```
(On Mac/Linux you may need `python3` instead of `python`.)

Tell Git who you are (one time):
```
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

---

## B. Start MySQL (ga-mysql)

Open Docker Desktop, then in a terminal:
```
docker run --name ga-mysql -e MYSQL_ROOT_PASSWORD=rootpass -p 3306:3306 -d mysql:8.4
```
Next time you only need: `docker start ga-mysql`

(If you installed MySQL normally instead of Docker, skip this step.)

---

## C. Create the database

1. Open DataGrip → **New → Data Source → MySQL**.
2. Host `localhost`, port `3306`, user `root`, password `rootpass`. Click **Test Connection** (download drivers if asked).
3. Open `setup.sql` from this folder, select everything, and run it.
4. Check: `SELECT * FROM sms.student;` should show 6 students.

---

## D. Put the project on your computer

1. Unzip this folder somewhere sensible, e.g. `Documents/student-management-system`.
2. Open the folder in PyCharm.
3. Open the terminal **inside PyCharm** (bottom bar) so you are in the project folder.

---

## E. Install the packages (pip)

Packages come from **PyPI** (https://pypi.org) and are installed with `pip`.
We put them in a *virtual environment* (`.venv`) so they belong to this project only.

Windows:
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
Mac / Linux:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` lists the two packages we need:
- `mysql-connector-python` – lets Python talk to MySQL
- `python-dotenv` – reads your password from `.env`

You will see `(.venv)` at the start of the terminal line when it is active.
In PyCharm: **Settings → Project → Python Interpreter** → choose the `.venv` one.

Need a new package later (e.g. Flask in Lecture 3)?
```
pip install flask
```
then add `flask` as a new line in `requirements.txt`.

---

## F. Make your .env and run app.py

1. Copy `.env` to a new file called `.env`.
2. Make sure the password in `.env` is the same as in `setup.sql` (`ChangeMe123!` unless you changed it).
3. Run:
```
python app.py
```
You should see:
```
Emma Berg emma@school.no
Ali Dahl ali@school.no
Amir Hassan amir@school.no
Nora Haugen nora@school.no
Sara Khan sara@school.no
Jonas Lie jonas@school.no
```

How the files work together:
```
app.py  ──asks──►  db.py (get_connection)  ──reads──►  .env
   │                                     └──connects──► MySQL (sms database)
   └── prints the students
```
In Lecture 2 you add `student_repo.py` between app.py and db.py.

---

## G. Create the Git repository and push to GitHub

### 1. Make it a Git repository (in the project folder)
```
git init -b main
git status
```
**Check:** `.env` must NOT be in the list (it is in `.gitignore`). If it is, stop and fix `.gitignore`.

### 2. First commit
```
git add .
git commit -m "Lecture 1: connect to MySQL and print the students"
```

### 3. Create the repository on GitHub
- Go to https://github.com/new
- Name: `student-management-system`
- **Do not** tick "Add a README" (you already have one)
- Click **Create repository**

### 4. Connect and push (copy your own URL from the GitHub page)
```
git remote add origin https://github.com/YOUR-USERNAME/student-management-system.git
git push -u origin main
```
The first time, Git asks you to log in (a browser window opens).
Refresh GitHub: your files are there, and `.env` is **not**.

---

## H. The commit routine (use it after every step in every lecture)

```
git status                      # 1. look: what changed? Is .env in the list? Then STOP.
git add app.py student_repo.py  # 2. choose the files to save
git commit -m "Short clear message about what you did"   # 3. save a version
git push                        # 4. send it to GitHub
```
Good messages: `"Add get_all_students() to student_repo.py"`, `"Add search by name to menu"`.
Bad messages: `"fix"`, `"stuff"`, `"asdf"`.

On another laptop: `git clone https://github.com/YOUR-USERNAME/student-management-system.git`
Before you start working: `git pull`

---

## I. Common problems

| Error | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'mysql'` | `.venv` not active, or you skipped `pip install -r requirements.txt` |
| `2003 Can't connect` | MySQL is not running: `docker start ga-mysql` |
| `1045 Access denied` | Password in `.env` is different from the one in `setup.sql` |
| `1146 Table doesn't exist` | You didn't run `setup.sql`, or a typo in the table name |
| `'python' is not recognized` | Reinstall Python and tick "Add to PATH", or use `py` on Windows |
| `git push` rejected | You ticked "Add README" on GitHub: run `git pull origin main --allow-unrelated-histories`, then push |
