"""The students department: every page whose address starts with /students."""
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from .validation import validate_student

import student_repo as repo

bp = Blueprint("students", __name__)


@bp.route("/students")
def student_list():
    """/students: every student.  /students?q=ha: only the students with "ha" in their name."""
    q = request.args.get("q", "").strip()
    if q:
        if len(q) < 2:
            abort(400, description="Please search for at least 2 letters.")
        students = repo.search_students(q)
    else:
        students = repo.get_all_students()
    return render_template("students.html", students=students, q=q)


@bp.route("/students/<int:student_id>")
def student_detail(student_id):
    """/students/1: one student."""
    student = repo.get_student(student_id)
    if student is None:
        abort(404)
    return render_template("student.html", student=student)


@bp.route("/students/new", methods=["GET", "POST"])
def student_new():
    form, errors = {}, {}
    if request.method == "POST":
        form, errors = validate_student(request.form)              # 1. check
        if not errors:
            try:
                new_id = repo.add_student(form["first_name"], form["last_name"],
                                          form["email"], form["class_name"])   # 2. save
            except repo.EmailTaken:
                errors["email"] = "Another student already has this email."
            else:
                flash(f"{form['first_name']} {form['last_name']} was added.", "success")
                return redirect(url_for("students.student_detail", student_id=new_id))   # 3. redirect
    return render_template("student_form.html", form=form, errors=errors)  # show the form (again)