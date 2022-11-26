from fastapi import APIRouter, Depends
from services import students as students_service
import schemas, models
from sqlalchemy.orm import Session
from typing import List
router = APIRouter(prefix="/students")


@router.post("/", tags=["students"])
async def create_student(student: schemas.StudentInsert, db: Session = Depends(models.get_db)):
    return students_service.create_student(student=student, db=db)

@router.get("/", tags=["students"],response_model=List[schemas.StudentWithSubjects],
response_model_by_alias=False,response_model_exclude={"note"})
async def get_all_students(db: Session = Depends(models.get_db)):
    return students_service.get_all_students(db=db)

@router.get("/{student_id}", tags=["students"],response_model=schemas.StudentWithSubjects,
response_model_by_alias=False,response_model_exclude={"note"})
async def get_student_by_id(student_id: str, db: Session = Depends(models.get_db)):
    return students_service.get_student_by_id(student_id=student_id, db=db)

@router.put("/{student_id}", tags=["students"])
async def update_student_by_id(student_id: str, student: schemas.StudentInsert,
                            db: Session = Depends(models.get_db)):
    return students_service.update_student(student_id=student_id, db=db, student=student)

@router.delete("/{student_id}", tags=["students"])
async def delete_student_by_id(student_id: str, db: Session = Depends(models.get_db)):
    return students_service.delete_student(student_id=student_id, db=db)

@router.delete("/", tags=["students"])
async def delete_all_students(db: Session = Depends(models.get_db)):
    return students_service.delete_all_students(db=db)


