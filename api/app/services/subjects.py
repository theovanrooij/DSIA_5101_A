from typing import List

from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException
from datetime import datetime
import models, schemas



def get_all_subjects(db: Session, skip: int = 0, limit: int = 200) -> List[schemas.SubjectWithStudents]:
    records = db.query(models.Subject).options(joinedload(models.Subject.students)).filter().offset(skip).limit(limit).all()
    return_list = []
    for record in records:
        record.id = str(record.id)
        return_list.append(schemas.SubjectWithStudents.from_orm(record))
    return return_list

def get_subject_by_id(subject_id: str, db: Session) -> models.Subject:
    record = db.query(models.Subject).filter(models.Subject.id == subject_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not Found") 
    record.id = str(record.id)
    return record

def get_subject_students_by_id(subject_id: str, db: Session) -> schemas.SubjectWithStudents:
    record = db.query(models.Subject).options(joinedload(models.Subject.student)).filter(models.Subject.id == subject_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not Found") 
    record.id = str(record.id)
    return schemas.SubjectWithStudents.from_orm(record)

def create_subject(db: Session, subject: schemas.SubjectWithStudents) -> models.Subject:

    from .students import get_student_by_id
    record = db.query(models.Subject).filter(models.Subject.id == subject.id).first()
    if record:
        raise HTTPException(status_code=409, detail="Already exists")

    subject_dict = subject.dict()
    students = subject_dict.pop("students")

    db_subject = models.Subject(**subject_dict)
    if students :
        for student in  students: 
            print(get_student_by_id(student,db))
            db_subject.students.append(get_student_by_id(student,db))
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    db_subject.id = str(db_subject.id)
    return db_subject


def update_subject(subject_id: str, db: Session, subject: schemas.SubjectWithStudents) -> models.Subject:
    from .students import get_student_by_id

    db_subject = get_subject_by_id(subject_id=subject_id, db=db)

    students = subject.subjects.copy()
    subject.students = list()


    for var, value in vars(subject).items():
        setattr(db_subject, var, value) if value else None

    db_subject.subjects = list()
    for student in  students: 
        db_subject.subjects.append(get_student_by_id(student,db))

    db_subject.updated_at = datetime.now()
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


def delete_subject(subject_id: str, db: Session) -> models.Subject:
    db_subject = get_subject_by_id(subject_id=subject_id, db=db)
    db.delete(db_subject)
    db.commit()
    return db_subject


def delete_all_subjects(db: Session) -> List[models.Subject]:
    records = db.query(models.Subject).filter()
    for record in records:
        db.delete(record)
    db.commit()
    return records