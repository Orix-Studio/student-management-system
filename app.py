"""app.py: a small menu. Only input() and print() here. All SQL is in student_repo.py."""
import mysql.connector
from student_repo import get_all_students, find_student, search_students

def print_student(s):
    print(f"{s['first_name']:>3} {s['last_name']:<8} {s['email']:<18} {s['class_name']}")


def show_all_students():
    students = get_all_students()
    if not students:
        print("No students registered yet.")
        return
    for s in students:
        print_student(s)
    print(f"\n{len(students)} students")


def show_one_student():
    email = input("Enter email: ").strip()
    student = find_student(email)
    if student is None:
        print("No student registered with this email.")
    else:
        print_student(student)


def search_student_name():
    name = input("Search student name: ").strip()
    students = search_students(name)
    if not students:
        print("No student with this name.")
    else:
        for s in students:
            print_student(s)
        print(f"\n{len(students)} students found for this search.")


def main():
    while True:
        print(f"\n=== Student Management System ===\n"
              f"1. Show all students\n"
              f"2. Find student by email\n"
              f"3. Search student by name\n"
              f"0. Quit")
        choice = input("Choose: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        try:
            if choice == "1":
                show_all_students()
            elif choice == "2":
                show_one_student()
            elif choice == "3":
                search_student_name()
            else:
                print("Please choose 1, 2 or 0.")
        except mysql.connector.Error as err:
            # The user gets one calm sentence, not the SQL details.
            print(f"Sorry, something went wrong with the database (error {err.errno}). Please try again later.")


if __name__ == "__main__":
    main()