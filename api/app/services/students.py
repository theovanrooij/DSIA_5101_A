from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
import models, schemas

def get_all_students(db: Session, skip: int = 0, limit: int = 10) -> List[models.Student]:
    records = db.query(models.Student).filter().offset(skip).limit(limit).all()
    for record in records:
        record.id = str(record.id)
    return records

def get_student_by_id(student_id: str, db: Session) -> models.Student:
    record = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not Found") 
    record.id = str(record.id)
    return record

def create_student(db: Session, student: schemas.Students) -> models.Student:
    record = db.query(models.Student).filter(models.Student.id == student.id).first()
    if record:
        raise HTTPException(status_code=409, detail="Already exists")
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    db_student.id = str(db_student.id)
    return db_student




def update_student(student_id: str, db: Session, student: schemas.Students) -> models.Student:
    db_student = get_student_by_id(student_id=student_id, db=db)
    for var, value in vars(student).items():
        setattr(db_student, var, value) if value else None
    db_student.updated_at = datetime.now()
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