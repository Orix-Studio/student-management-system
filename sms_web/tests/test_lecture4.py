"""Today's scoreboard: 7 small tests. Run: pytest -v
Needs ga-mysql running and the six students from setup.sql."""
import re

import student_repo as repo
from sms_web import create_app
from sms_web.validation import validate_student

GOOD = {"first_name": "Test", "last_name": "Person", "email": "form.test@example.com", "class_name": "2A"}


def client():
    app = create_app()
    app.config["SECRET_KEY"] = app.config.get("SECRET_KEY") or "only-for-tests"
    return app.test_client()


def test_about_page():                                   # Part 1
    assert "Our classes" in client().get("/about").data.decode()


def test_menu_on_every_page():                           # Part 2
    assert 'href="/about"' in client().get("/students").data.decode()


def test_classes_page():                                 # Parts 3, 4 and 5
    html = client().get("/classes").data.decode()
    assert "2A" in html and "2B" in html


def test_validate_cleans_the_data():                     # Part 7
    data, errors = validate_student({"first_name": " Emma ", "last_name": "Larsen",
                                     "email": " Emma@School.NO ", "class_name": "2a"})
    assert errors == {}
    assert data["first_name"] == "Emma" and data["email"] == "emma@school.no" and data["class_name"] == "2A"


def test_validate_finds_the_errors():                    # Part 7
    _, errors = validate_student({"first_name": "", "email": "emma", "class_name": "3C"})
    assert set(errors) == {"first_name", "last_name", "email", "class_name"}


def test_add_student_redirects_and_flashes():            # Parts 6 and 7
    c = client()
    response = c.post("/students/new", data=GOOD)
    assert response.status_code == 302                   # Post/Redirect/Get
    new_id = int(re.search(r"/students/(\d+)$", response.headers["Location"]).group(1))
    try:
        assert "Test Person was added." in c.get(f"/students/{new_id}").data.decode()
    finally:
        repo.delete_student(new_id)                      # clean up


def test_errors_are_shown_and_values_kept():             # Part 7
    html = client().post("/students/new", data={**GOOD, "last_name": "", "email": "emma@"}).data.decode()
    assert "Last name is required." in html
    assert 'value="Test"' in html                        # the user's typing is still there