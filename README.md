# Student API

A backend-only FastAPI application for adding, listing, looking up, and deleting students.

## Requirements

- Python 3.10 or newer
- Packages listed in `requirements.txt`:
  - `fastapi` for the API framework
  - `uvicorn[standard]` to run the application
  - `pytest` for tests
  - `httpx` for FastAPI's test client

## Setup

Run these commands from the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run the API

```powershell
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## API endpoints

All student endpoints use the `/api/v1/students` prefix.

| Method | Path | Description | Success response |
| --- | --- | --- | --- |
| `POST` | `/api/v1/students` | Add a student | `201` and the created student |
| `GET` | `/api/v1/students` | View all students | `200` and a list |
| `GET` | `/api/v1/students/{student_id}` | View a student by ID | `200` and the student |
| `DELETE` | `/api/v1/students/{student_id}` | Delete a student | `204` |

New students require a `name`, positive integer `age`, and `grade`. For example:

```json
{
  "name": "Asha",
  "age": 20,
  "grade": "Year 2"
}
```

Student data is held in memory and is cleared whenever the application restarts. Requests for a nonexistent student return `404`.

## Run tests

```powershell
pytest
```
