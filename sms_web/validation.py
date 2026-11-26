"""Checks the data from the student form. Pure Python, so it is easy to test."""


def validate_student(form):
    """Returns two things: the cleaned data, and a dict of errors (empty = all OK)."""
    data = {
        "first_name": form.get("first_name", "").strip(),
        "last_name": form.get("last_name", "").strip(),
        "email": form.get("email", "").strip().lower(),
        "class_name": form.get("class_name", "").strip().upper(),
    }
    errors = {}
    if not data["first_name"]:
        errors["first_name"] = "First name is required."
    if not data["last_name"]:
        errors["last_name"] = "Last name is required."
    if "@" not in data["email"] or "." not in data["email"]:
        errors["email"] = "Please enter a valid email, like name@school.no."
    if data["class_name"] not in ("2A", "2B"):
        errors["class_name"] = "Please choose 2A or 2B."
    if len(data["first_name"]) > 50:
        errors["first_name"] = "First name must be less than 50 characters."
    return data, errors