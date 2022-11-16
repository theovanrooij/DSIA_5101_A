from fastapi import APIRouter, Depends
from services import subjects as subjects_service
import schemas, models
from sqlalchemy.orm import Session

router = APIRouter(prefix="/subjects")


@router.post("/", tags=["subjects"])
async def create_subject(subject: schemas.Subjects, db: Session = Depends(models.get_db)):
    print(subject)
    return subjects_service.create_subject(subject=subject, db=db)


@router.get("/", tags=["subjects"])
async def get_all_subjects(db: Session = Depends(models.get_db)):
    return subjects_service.get_all_subjects(db=db)


@router.get("/{subject_id}", tags=["subjects"])
async def get_subject_by_id(subject_id: str, db: Session = Depends(models.get_db)):
    return subjects_service.get_subject_by_id(subject_id=subject_id, db=db)


@router.put("/{subject_id}", tags=["subjects"])
async def update_subject_by_id(subject_id: str, subject: schemas.Subjects,
                            db: Session = Depends(models.get_db)):
    return subjects_service.update_subject(subject_id=subject_id, db=db, subject=subject)


@router.delete("/{subject_id}", tags=["subjects"])
async def delete_subject_by_id(subject_id: str, db: Session = Depends(models.get_db)):
    return subjects_service.delete_subject(subject_id=subject_id, db=db)


@router.delete("/", tags=["subjects"])
async def delete_all_subjects(db: Session = Depends(models.get_db)):
    return subjects_service.delete_all_subjects(db=db)


