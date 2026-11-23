import mysql.connector
from mysql.connector import errorcode

from db import get_connection


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