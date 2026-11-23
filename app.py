"""app.py: a small menu. Only input() and print() here. All SQL is in student_repo.py."""
from student_repo import get_all_students, find_student

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


def main():
    while True:
        print(f"\n=== Student Management System ===\n"
              f"1. Show all students\n"
              f"2. Find student by email\n"
              f"0. Quit")
        choice = input("Choose: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "1":
            show_all_students()
        elif choice == "2":
            show_one_student()
        else:
            print("Please choose 1, 2 or 0.")


if __name__ == "__main__":
    main()