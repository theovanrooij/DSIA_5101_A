from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
import models, schemas

def get_all_subjects(db: Session, skip: int = 0, limit: int = 10) -> List[models.Subject]:
    records = db.query(models.Subject).filter().offset(skip).limit(limit).all()
    for record in records:
        record.id = str(record.id)
    return records

def get_subject_by_id(subject_id: str, db: Session) -> models.Subject:
    record = db.query(models.Subject).filter(models.Subject.id == subject_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not Found") 
    record.id = str(record.id)
    return record

def create_subject(db: Session, subject: schemas.Subjects) -> models.Subject:
    record = db.query(models.Subject).filter(models.Subject.id == subject.id).first()
    if record:
        raise HTTPException(status_code=409, detail="Already exists")
    db_subject = models.Student(**subject.dict())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    db_subject.id = str(db_subject.id)
    return db_subject


def update_subject(subject_id: str, db: Session, subject: schemas.Subjects) -> models.Subject:
    db_subject = get_subject_by_id(subject_id=subject_id, db=db)
    for var, value in vars(subject).items():
        setattr(db_subject, var, value) if value else None
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