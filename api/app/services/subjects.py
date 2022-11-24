from typing import List

from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException
from datetime import datetime
import models, schemas
from models import StudentSubject


def get_all_subjects(db: Session, skip: int = 0, limit: int = 200) -> List[models.Subject]:
    # records = db.query(models.Subject).options(joinedload(models.Subject.students).options(joinedload(models.StudentSubject.student))).filter().offset(skip).limit(limit).all()
    db_subject = db.query(models.Subject).options(joinedload(models.Subject.students)).filter().offset(skip).limit(limit).all()
    print(db_subject)

    for record in db_subject:
        record.id = str(record.id)
        for student in record.students:
            student.student_id = str(student.student_id)
    return db_subject
        # return_list.append(schemas.SubjectWithStudents.from_orm(record))

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
    note = subject_dict.pop("note")
    print(subject_dict)
    db_subject = models.Subject(**subject_dict)

    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)

    relation_list = list()
    if students :
        for student in  students: 
            if len(student) == 2 :
                note = student[1]
            else:
                note = None

            db_student = get_student_by_id(student[0],db)
            relation_list.append(StudentSubject(subject_id=db_subject.id,student_id=db_student.id,note=note))
            # student_db = get_student_by_id(student,db)
            # db_subject.students.append(student_db)

    print(relation_list,students)
    db.add_all(relation_list)
    db.commit()
    db.refresh(db_subject)
    db_subject.id = str(db_subject.id)
    return db_subject


def update_subject(subject_id: str, db: Session, subject: schemas.SubjectWithStudents) -> models.Subject:
    from .students import get_student_by_id

    db_subject = get_subject_by_id(subject_id=subject_id, db=db)

    students = subject.students.copy()
    subject.students.clear()


    for var, value in vars(subject).items():
        setattr(db_subject, var, value) if value else None

    db_subject.students.clear()
    for student in  students: 
        db_subject.students.append(get_student_by_id(student,db))

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