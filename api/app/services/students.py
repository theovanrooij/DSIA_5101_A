from typing import List

from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException
from datetime import datetime
import models, schemas


def get_all_students(db: Session, skip: int = 0, limit: int = 200) -> List[schemas.StudentWithSubjects]:
    records = db.query(models.Student).options(joinedload(models.Student.subjects)).filter().offset(skip).limit(limit).all()
    return_list = []
    for record in records:
        record.id = str(record.id)
        return_list.append(schemas.StudentWithSubjects.from_orm(record))
    return return_list

def get_student_by_id(student_id: str, db: Session) -> models.Student:
    record = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not Found") 
    record.id = str(record.id)
    return record

def get_student_subjects_by_id(student_id: str, db: Session) -> schemas.StudentWithSubjects:
    record = db.query(models.Student).options(joinedload(models.Student.subjects)).filter(models.Student.id == student_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not Found") 
    record.id = str(record.id)
    return schemas.StudentWithSubjects.from_orm(record)

def create_student(db: Session, student: schemas.StudentWithSubjects) -> models.Student:
    from .subjects import get_subject_by_id
    record = db.query(models.Student).filter(models.Student.id == student.id).first()
    if record:
        raise HTTPException(status_code=409, detail="Already exists")

    student_dict = student.dict()
    subjects = student_dict.pop("subjects")

    db_student = models.Student(**student_dict)
    if subjects :
        for subject in subjects: 
            db_student.subjects.append(get_subject_by_id(subject,db))

    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    db_student.id = str(db_student.id)
    return db_student


def update_student(student_id: str, db: Session, student: schemas.StudentWithSubjects) -> models.Student:
    from .subjects import get_subject_by_id

    db_student = get_student_by_id(student_id=student_id, db=db) 
    print(db_student)
    subjects = student.subjects.copy()
    student.subjects.clear()

    for var, value in vars(student).items():
        setattr(db_student, var, value) if value else None

    db_student.subjects.clear()
    for subject in  subjects: 
        db_student.subjects.append(get_subject_by_id(subject,db))

    db_student.updated_at = datetime.now()
    print(db_student)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(student_id: str, db: Session) -> models.Student:
    db_student = get_student_by_id(student_id=student_id, db=db)
    # return db_student
    db.delete(db_student)
    db.commit()
    return db_student


def delete_all_students(db: Session) -> List[models.Student]:
    records = db.query(models.Student).filter()
    for record in records:
        db.delete(record)
    db.commit()
    return records