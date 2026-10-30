from threading import Lock

from app.schemas import StudentCreate, StudentRead


class StudentStore:
    """Thread-safe in-memory storage for student records."""

    def __init__(self) -> None:
        self._students: dict[int, StudentRead] = {}
        self._next_id = 1
        self._lock = Lock()

    def add(self, student: StudentCreate) -> StudentRead:
        with self._lock:
            student_record = StudentRead(id=self._next_id, **student.model_dump())
            self._students[self._next_id] = student_record
            self._next_id += 1
            return student_record

    def list(self) -> list[StudentRead]:
        with self._lock:
            return list(self._students.values())

    def get(self, student_id: int) -> StudentRead | None:
        with self._lock:
            return self._students.get(student_id)

    def delete(self, student_id: int) -> bool:
        with self._lock:
            return self._students.pop(student_id, None) is not None
