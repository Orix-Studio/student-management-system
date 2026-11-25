"""app.py: a small menu. Only input() and print() here. All SQL is in student_repo.py."""
import mysql.connector
from student_repo import EmailTaken, NotFound, get_all_students, find_student, search_students, add_student, count_students, get_class_names, get_newest_students, change_class, change_email, delete_student, search_students_in_class

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


def register_student():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email: ")
    class_name = input("Enter class name: ")

    try:
        new_id = add_student(first_name, last_name, email, class_name)
        print(f"Welcome {first_name.strip()}! You are student #{new_id}.")
    except EmailTaken:
        print("Email already registered.")
    except ValueError as err:
        print(err)


def ask_int(question):
    """Ask until user types a whole number (ready-made helper)."""
    while True:
        answer = input(question).strip()
        try:
            if int(answer) < 1:
                raise ValueError("Number must be greater than 0.")
            return int(answer)
        except ValueError:
            print("Please enter a whole number.")


def show_statistics():
    student_count = count_students()

    class_names = get_class_names()
    class_names_str = f""
    class_names_count = len(class_names)
    for class_name in class_names:
        class_names_str += f"{class_name}, "
    class_names_str = class_names_str[:-2]

    limit = ask_int("How many students do you want to show? ")
    newest_students = get_newest_students(limit)

    print(f"{student_count} students in {class_names_count} classes: {class_names_str}.\n"
          f"{limit} newest students:")
    for s in newest_students:
        print(f"{s['student_id']:>2} {s['first_name']} {s['last_name']}")


def move_student_to_class():
    student_id = ask_int("Enter student ID: ")
    class_name = input("Enter class name: ")

    try:
        change_class(student_id, class_name)
    except NotFound:
        print(f"No student registered with ID: {student_id}.")
    except ValueError:
        print("Class name must be between 1 and 10 characters.")


def change_student_email():
    student_id = ask_int("Enter student ID: ")
    email = input("Enter email: ")

    try:
        change_email(student_id, email)
    except NotFound:
        print(f"No student registered with ID: {student_id}.")
    except EmailTaken:
        print(f"Email already registered.")
    except ValueError:
        print("A student email must be given.")


def delete_one_student():
    student_id = ask_int("Enter student ID: ")
    confirm_delete = input(f"Are you sure you want to delete this student {student_id}? (y/n) ")
    if confirm_delete == "y":
        try:
            delete_student(student_id)
        except NotFound:
            print(f"No student registered with ID: {student_id}.")
        # No need for ValueError as ask_int() makes sure a positive number is entered by the user.
    else:
        print("Confirmation failed. No student was deleted.")


def search_for_class_students():
    word = input("Search for student: ")
    class_name = input("Enter class name: ")
    search_results = search_students_in_class(word, class_name)

    if search_results:
        for first_name, last_name in search_results:
            print(f"{first_name} {last_name}")
    else:
        print("No students found for this search.")



def main():
    while True:
        print(f"\n=== Student Management System ===\n"
              f"1. Show all students\n"
              f"2. Find student by email\n"
              f"3. Search student by name\n"
              f"4. Register student\n"
              f"5. Show statistics\n"
              f"6. Move student to another class\n"
              f"7. Change student email\n"
              f"8. Delete a student\n"
              f"9. Search for student in a class\n"
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
            elif choice == "4":
                register_student()
            elif choice == "5":
                show_statistics()
            elif choice == "6":
                move_student_to_class()
            elif choice == "7":
                change_student_email()
            elif choice == "8":
                delete_one_student()
            elif choice == "9":
                search_for_class_students()
            else:
                print("Please choose a number from 1-9 or 0.")
        except mysql.connector.Error as err:
            # The user gets one calm sentence, not the SQL details.
            print(f"Sorry, something went wrong with the database (error {err.errno}). Please try again later.")


if __name__ == "__main__":
    main()