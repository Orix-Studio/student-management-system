import mysql.connector
from mysql.connector import errorcode

from db import get_connection



# =============== Lecture 2 ===============

class EmailTaken(Exception):
    """Another student already has that email."""


def get_all_students():
    """Return every student as a list of dicts, sorted by last name."""
    conn = get_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT *
            FROM student
            ORDER BY last_name ASC
        """)
        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


def find_student(email):
    """Return one student as a dict, or None if no student has that email."""
    conn = get_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT *
            FROM student
            WHERE email = %s
        """
        cursor.execute(sql, (email,))
        return cursor.fetchone()

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


def search_students(word):
    """Return the students whose first or last name contains `word`, sorted by last name."""
    pattern = f"%{word}%"
    conn = get_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT *
            FROM student
            WHERE first_name LIKE %s OR last_name LIKE %s
            ORDER BY last_name, first_name
        """
        cursor.execute(sql, (pattern, pattern))
        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


def add_student(first_name, last_name, email, class_name):
    """Add a student and return the new student_id.
    Raise ValueError if a field is empty, and EmailTaken if the email is already in use."""

    first_name = first_name.strip().capitalize()
    last_name = last_name.strip().capitalize()
    email = email.strip().lower()
    class_name = class_name.strip().upper()
    if not first_name or not last_name or not email or not class_name:
        raise ValueError("Please fill out every field.")

    conn = get_connection()
    cursor = None

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO student (first_name, last_name, email, class_name) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, email, class_name)
        )
        conn.commit()
        return cursor.lastrowid

    except mysql.connector.Error as err:
        conn.rollback()
        if err.errno == errorcode.ER_DUP_ENTRY:
            raise EmailTaken(f"{email} is already registered") from err
        raise

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()




# =============== Practice day ===============

class NotFound(Exception):
    """There is no student with that id."""


def _student_exists(cursor, student_id):
    """Helper (ready-made): True if a student with this id exists. Used by change_class() and change_email()."""
    cursor.execute("SELECT 1 FROM student WHERE student_id = %s", (student_id,))
    return cursor.fetchone() is not None


# ---------- Station 1: read ----------

def count_students():
    """Return the number of students, as an int."""
    conn = get_connection()
    cursor = None

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM student")
        return cursor.fetchone()[0]

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


def get_class_names():
    """Return every class name once, sorted, as a list of strings: ['2A', '2B']."""
    conn = get_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT class_name
            FROM student
            GROUP BY class_name
            ORDER BY class_name
        """)
        return [row["class_name"] for row in cursor.fetchall()]

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


def get_newest_students(limit):
    """Return the `limit` newest students (highest student_id first). Raise ValueError if limit is less than 1."""
    if limit < 1:
        raise ValueError("limit must be greater than 0")

    conn = get_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
                SELECT student_id, first_name, last_name
                FROM student
                ORDER BY student_id DESC
                LIMIT %s
            """, (limit,))
        return cursor.fetchall()


    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


def email_exists(email):
    """Return True if a student has this email. Spaces and upper case don't matter."""
    raw_email = email.strip().lower()
    conn = get_connection()
    cursor = None

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT *
            FROM student
            WHERE email = %s
        """, (raw_email,))

        if cursor.fetchone() is not None:
            return True

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


# ---------- Station 2: search ----------

def search_students_in_class(word, class_name):
    """Return the students in one class whose first or last name contains `word`, sorted by last name."""
    name_pattern = f"%{word}%"

    conn = get_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT last_name
            FROM student
            WHERE (first_name LIKE %s OR last_name LIKE %s) AND class_name LIKE %s
        """, (name_pattern, name_pattern, class_name))
        return [row["last_name"] for row in cursor.fetchall()]

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


SORT_COLUMNS = {
    "name": "last_name, first_name",
    "first_name": "first_name, last_name",
    "class": "class_name, last_name, first_name",
}


def get_students_sorted(sort="name"):
    """Return every student, sorted the way the user chose. An unknown sort uses "name"."""
    order_by = SORT_COLUMNS.get(sort, SORT_COLUMNS["name"])

    conn = get_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"""
            SELECT first_name, last_name, class_name
            FROM student
            ORDER BY {order_by}
        """)
        return [f"{row['first_name']} {row['last_name']} ({row['class_name']})" for row in cursor.fetchall()]

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


# ---------- Station 3: change and delete ----------

def change_class(student_id, new_class):
    """UPDATE: move a student to another class.
    Raise ValueError if the class is empty or longer than 10 characters, and NotFound for an unknown id.
    """
    # TODO
    raise NotImplementedError


def change_email(student_id, new_email):
    """UPDATE: give a student a new email.
    Raise ValueError if it is empty, NotFound for an unknown id, and EmailTaken if another student has it.
    """
    # TODO
    raise NotImplementedError


def delete_student(student_id):
    """DELETE: remove a student. Raise NotFound if there was no student with that id."""
    # TODO
    raise NotImplementedError