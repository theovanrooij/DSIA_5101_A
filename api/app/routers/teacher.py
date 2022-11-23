from fastapi import APIRouter, Depends
from services import teachers as teachers_service
import schemas, models
from sqlalchemy.orm import Session

router = APIRouter(prefix="/teachers")


@router.post("/", tags=["teachers"])
async def create_student(teacher: schemas.TeacherWithSubjects, db: Session = Depends(models.get_db)):
    return teachers_service.create_teacher(teacher=teacher, db=db)


@router.get("/", tags=["teachers"])
async def get_all_teachers(db: Session = Depends(models.get_db)):
    return teachers_service.get_all_teachers(db=db)


@router.get("/{teacher_id}", tags=["teachers"])
async def get_teacher_by_id(teacher_id: str, db: Session = Depends(models.get_db)):
    return teachers_service.get_teacher_by_id(teacher_id=teacher_id, db=db)


@router.put("/{teacher_id}", tags=["teachers"])
async def update_teacher_by_id(teacher_id: str, teacher: schemas.TeacherWithSubjects,
                            db: Session = Depends(models.get_db)):
    return teachers_service.update_teacher(teacher_id=teacher_id, db=db, teacher=teacher)



@router.delete("/{teacher_id}", tags=["teachers"])
async def delete_teacher_by_id(teacher_id: str, db: Session = Depends(models.get_db)):
    return teachers_service.delete_teacher(teacher_id=teacher_id, db=db)


@router.delete("/", tags=["teachers"])
async def delete_all_teachers(db: Session = Depends(models.get_db)):
    return teachers_service.delete_all_teachers(db=db)


