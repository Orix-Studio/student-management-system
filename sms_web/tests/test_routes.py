"""The scoreboard for today. Run it from the project folder: pytest -v
It needs ga-mysql running and the six students from setup.sql.
"""
import pytest

from sms_web import create_app


@pytest.fixture
def client():
    return create_app().test_client()     # asks for pages like a browser, without starting a server


def test_home(client):
    assert client.get("/").status_code == 200


def test_student_list(client):
    page = client.get("/students")
    assert page.status_code == 200
    assert b"Hassan" in page.data


def test_unknown_page(client):
    assert client.get("/nope").status_code == 404


def test_student_id_must_be_a_number(client):
    assert client.get("/students/amir").status_code == 404


def test_class_list(client):                                   # Task 2
    page = client.get("/classes")
    assert page.status_code == 200
    assert b"2A" in page.data and b"2B" in page.data
    assert b"3 students" in page.data


def test_student_detail(client):                               # Task 3
    page = client.get("/students/1")
    assert page.status_code == 200
    assert b"Amir Hassan" in page.data
    assert b"amir@school.no" in page.data


def test_student_unknown(client):                              # Task 3
    assert client.get("/students/999").status_code == 404


def test_class_detail(client):                                 # Task 4
    page = client.get("/classes/2B")
    assert page.status_code == 200
    assert b"Jonas Lie" in page.data
    assert b"Amir" not in page.data


def test_class_lower_case(client):                             # Task 4
    page = client.get("/classes/2b")
    assert page.status_code == 200
    assert b"Jonas Lie" in page.data


def test_class_unknown(client):                                # Task 4
    assert client.get("/classes/9Z").status_code == 404


def test_search(client):                                       # Task 5
    page = client.get("/students?q=ha")
    assert b"Hassan" in page.data and b"Khan" in page.data
    assert b"Berg" not in page.data


def test_search_too_short(client):                             # Task 5
    assert client.get("/students?q=a").status_code == 400