from db import get_connection


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