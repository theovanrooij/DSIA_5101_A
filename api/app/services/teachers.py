from typing import List

from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException
from datetime import datetime
import models, schemas


def get_all_teachers(db: Session, skip: int = 0, limit: int = 200) -> List[schemas.TeacherWithSubjects]:
    records = db.query(models.Teacher).options(joinedload(models.Teacher.subjects)).filter().offset(skip).limit(limit).all()
    return_list = []
    for record in records:
        record.id = str(record.id)
        return_list.append(schemas.TeacherWithSubjects.from_orm(record))
    return return_list


def get_teacher_by_id(teacher_id: str, db: Session) -> models.Teacher:
    record = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not Found") 
    record.id = str(record.id)
    return record


def get_teacher_subjects_by_id(teacher_id: str, db: Session) -> schemas.TeacherWithSubjects:
    record = db.query(models.Teacher).options(joinedload(models.Teacher.subjects)).filter(models.Teacher.id == teacher_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not Found") 
    record.id = str(record.id)
    return schemas.TeacherWithSubjects.from_orm(record)


def create_teacher(db: Session, teacher: schemas.TeacherWithSubjects) -> models.Teacher:
    from .subjects import get_subject_by_id
    record = db.query(models.Teacher).filter(models.Teacher.id == teacher.id).first()
    if record:
        raise HTTPException(status_code=409, detail="Already exists")

    teacher_dict = teacher.dict()
    subjects = teacher_dict.pop("subjects")

    db_teacher = models.Teacher(**teacher_dict)
    if subjects :
        for subject in subjects: 
            db_teacher.subjects.append(get_subject_by_id(subject,db))

    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    db_teacher.id = str(db_teacher.id)
    return db_teacher


def update_teacher(teacher_id: str, db: Session, teacher: schemas.TeacherWithSubjects) -> models.Teacher:
    from .subjects import get_subject_by_id

    db_teacher = get_teacher_by_id(teacher_id=teacher_id, db=db) 
    
    subjects = teacher.subjects
    if subjects :
        subjects = subjects.copy()
        teacher.subjects.clear()

    for var, value in vars(teacher).items():
        setattr(db_teacher, var, value) if value else None

    db_teacher.subjects.clear()
    if subjects :
        for subject in  subjects: 
            db_teacher.subjects.append(get_subject_by_id(subject,db))
    
    db_teacher.updated_at = datetime.now()
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


def delete_teacher(teacher_id: str, db: Session) -> models.Teacher:
    db_teacher = get_teacher_by_id(teacher_id=teacher_id, db=db)
    db.delete(db_teacher)
    db.commit()
    return db_teacher


def delete_all_teachers(db: Session) -> List[models.Teacher]:
    records = db.query(models.Teacher).filter()
    for record in records:
        db.delete(record)
    db.commit()
    return records