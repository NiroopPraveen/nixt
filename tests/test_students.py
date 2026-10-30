import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import students
from app.store import StudentStore

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_student_store(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(students, "student_store", StudentStore())


def test_add_student() -> None:
    response = client.post(
        "/api/v1/students",
        json={"name": "Asha", "age": 20, "grade": "Year 2"},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Asha",
        "age": 20,
        "grade": "Year 2",
    }


def test_add_student_rejects_invalid_data() -> None:
    response = client.post(
        "/api/v1/students",
        json={"name": "", "age": 0, "grade": ""},
    )

    assert response.status_code == 422


def test_view_all_students() -> None:
    client.post(
        "/api/v1/students",
        json={"name": "Asha", "age": 20, "grade": "Year 2"},
    )
    client.post(
        "/api/v1/students",
        json={"name": "Ravi", "age": 21, "grade": "Year 3"},
    )

    response = client.get("/api/v1/students")

    assert response.status_code == 200
    assert [student["name"] for student in response.json()] == ["Asha", "Ravi"]


def test_view_student_by_id() -> None:
    created = client.post(
        "/api/v1/students",
        json={"name": "Asha", "age": 20, "grade": "Year 2"},
    ).json()

    response = client.get(f"/api/v1/students/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_view_missing_student_returns_not_found() -> None:
    response = client.get("/api/v1/students/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Student not found"}


def test_delete_student() -> None:
    created = client.post(
        "/api/v1/students",
        json={"name": "Asha", "age": 20, "grade": "Year 2"},
    ).json()

    response = client.delete(f"/api/v1/students/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/api/v1/students/{created['id']}").status_code == 404


def test_delete_missing_student_returns_not_found() -> None:
    response = client.delete("/api/v1/students/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Student not found"}
