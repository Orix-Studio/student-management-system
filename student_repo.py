from db import get_connection


def get_all_students():
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