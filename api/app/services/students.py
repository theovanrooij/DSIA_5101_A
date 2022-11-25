from typing import List

from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException
from datetime import datetime
import models, schemas


def get_all_students(db: Session, skip: int = 0, limit: int = 200) -> List[models.Student]:
    records = db.query(models.Student).options(joinedload(models.Student.subjects)).filter().offset(skip).limit(limit).all()
    for record in records:
        record.id = str(record.id)
        for subject in record.subjects:
            subject.subject_id = str(subject.subject_id)
    return records

def get_student_by_id(student_id: str, db: Session) -> models.Student:
    record = db.query(models.Student).options(joinedload(models.Student.subjects)).filter(models.Student.id == student_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not Found") 
    record.id = str(record.id)
    for subject in record.subjects:
        subject.subject_id = str(subject.subject_id)
    return record

def get_student_subjects_by_id(student_id: str, db: Session) -> schemas.StudentWithSubjects:
    record = db.query(models.Student).options(joinedload(models.Student.subjects)).filter(models.Student.id == student_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not Found") 
    record.id = str(record.id)
    return schemas.StudentWithSubjects.from_orm(record)

def create_student(db: Session, student: schemas.StudentInsert) -> models.Student:
    from .subjects import get_subject_by_id
    record = db.query(models.Student).filter(models.Student.id == student.id).first()
    if record:
        raise HTTPException(status_code=409, detail="Already exists")

    student_dict = student.dict()
    subjects = student_dict.pop("subjects")
    note = student_dict.pop("note")
    db_student = models.Student(**student_dict)

    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    
    relation_list = list()
    if subjects :
        for subject in  subjects: 
            note = subject[1]
            if note == -1 : 
                note = None

            db_subject = get_subject_by_id(subject[0],db)
            relation_list.append(models.StudentSubject(subject_id=db_subject.id,student_id=db_student.id,note=note))
    db.add_all(relation_list)
    db.commit()
    db.refresh(db_student)
    db_student.id = str(db_student.id)
    return db_student

def update_student(student_id: str, db: Session, student: schemas.StudentInsert) -> models.Student:
    from .subjects import get_subject_by_id

    db_student = get_student_by_id(student_id=student_id, db=db) 

    subjects = student.subjects 
    if subjects :
        subjects = subjects.copy()
        student.subjects.clear()
    
    for var, value in vars(student).items():
        setattr(db_student, var, value) if value else None

    for subject in db_student.subjects : 
        db.delete(subject)
    
    db_student.updated_at = datetime.now()
    db.commit()
    db.refresh(db_student)

    if subjects :
        for subject in  subjects: 
            note = subject[1]
            if note == -1 : 
                note = None
            db_subject = get_subject_by_id(subject[0],db)
            db_student.subjects.append(models.StudentSubject(subject_id=db_subject.id,student_id=db_student.id,note=note))

    
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
    return db_student


def delete_student(student_id: str, db: Session) -> models.Student:
    db_student = get_student_by_id(student_id=student_id, db=db)
    db.delete(db_student)
    db.commit()
    return db_student


def delete_all_students(db: Session) -> List[models.Student]:
    records = db.query(models.Student).filter()
    for record in records:
        db.delete(record)
    db.commit()
    return records