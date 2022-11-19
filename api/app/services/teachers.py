from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
import models, schemas

def get_all_teachers(db: Session, skip: int = 0, limit: int = 10) -> List[models.Teacher]:
    records = db.query(models.Teacher).filter().offset(skip).limit(limit).all()
    for record in records:
        record.id = str(record.id)
    return records

def get_teacher_by_id(teacher_id: str, db: Session) -> models.Teacher:
    record = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not Found") 
    record.id = str(record.id)
    return record

def create_teacher(db: Session, teacher: schemas.Teachers) -> models.Teacher:
    print(teacher)
    record = db.query(models.Teacher).filter(models.Teacher.id == teacher.id).first()
    if record:
        raise HTTPException(status_code=409, detail="Already exists")
    db_teacher = models.Teacher(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    db_teacher.id = str(db_teacher.id)
    return db_teacher

def update_teacher(teacher_id: str, db: Session, teacher: schemas.Teachers) -> models.Teacher:
    db_teacher = get_teacher_by_id(teacher_id=teacher_id, db=db)
    for var, value in vars(teacher).items():
        setattr(db_teacher, var, value) if value else None
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