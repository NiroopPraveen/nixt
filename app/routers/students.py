from fastapi import APIRouter, HTTPException, Response, status

from app.schemas import StudentCreate, StudentRead
from app.store import StudentStore

router = APIRouter(prefix="/students", tags=["students"])
student_store = StudentStore()


@router.post(
    "",
    response_model=StudentRead,
    status_code=status.HTTP_201_CREATED,
)
def add_student(student: StudentCreate) -> StudentRead:
    return student_store.add(student)


@router.get("", response_model=list[StudentRead])
def view_students() -> list[StudentRead]:
    return student_store.list()


@router.get("/{student_id}", response_model=StudentRead)
def view_student(student_id: int) -> StudentRead:
    student = student_store.get(student_id)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int) -> Response:
    if not student_store.delete(student_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
