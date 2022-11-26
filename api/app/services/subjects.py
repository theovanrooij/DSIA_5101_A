from typing import List

from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException
from datetime import datetime
import models, schemas
from models import StudentSubject


def get_all_subjects(db: Session, skip: int = 0, limit: int = 200) -> List[models.Subject]:
    db_subject = db.query(models.Subject).options(joinedload(models.Subject.students)).filter().offset(skip).limit(limit).all()
    for record in db_subject:
        record.id = str(record.id)
        for student in record.students:
            student.student_id = str(student.student_id)
        for teacher in record.teachers:
            teacher.id = str(teacher.id)


    return db_subject

def get_subject_by_id(subject_id: str, db: Session) -> models.Subject:
    record = db.query(models.Subject).options(joinedload(models.Subject.students)).filter(models.Subject.id == subject_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not Found")         
    return record

def create_subject(db: Session, subject: schemas.SubjectInsert) -> models.Subject:

    from .students import get_student_by_id
    from .teachers import get_teacher_by_id
    record = db.query(models.Subject).filter(models.Subject.id == subject.id).first()
    if record:
        raise HTTPException(status_code=409, detail="Already exists")

    subject_dict = subject.dict()
    students = subject_dict.pop("students")
    note = subject_dict.pop("note")
    teachers = subject_dict.pop("teachers")


    db_subject = models.Subject(**subject_dict)

    if teachers :
        for teacher in teachers: 
            db_subject.teachers.append(get_teacher_by_id(teacher,db))

    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)

    relation_list = list()
    if students :
        for student in  students: 
            note = student[1]
            if note == -1 : 
                note = None

            db_student = get_student_by_id(student[0],db)
            relation_list.append(models.StudentSubject(subject_id=db_subject.id,student_id=db_student.id,note=note))
    db.add_all(relation_list)
    db.commit()
    db.refresh(db_subject)
    db_subject.id = str(db_subject.id)

    return db_subject

def update_subject(subject_id: str, db: Session, subject: schemas.SubjectInsert) -> models.Subject:
    from .students import get_student_by_id 
    from .teachers import get_teacher_by_id

    db_subject = get_subject_by_id(subject_id=subject_id, db=db)

    students = subject.students
    
    if students :
        students = students.copy()
        subject.students.clear()
        
    teachers = subject.teachers.copy()
    subject.teachers.clear()

    for var, value in vars(subject).items():
        setattr(db_subject, var, value) if value else None

    db_subject.teachers.clear()
    for student in  teachers: 
        db_subject.teachers.append(get_teacher_by_id(student,db))
    
    for student in db_subject.students : 
        db.delete(student)
    
    db_subject.updated_at = datetime.now()
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    
    if students :
        for student in  students: 
            note = student[1]
            if note == -1 : 
                note = None

            db_student = get_student_by_id(student[0],db)
            db_subject.students.append(models.StudentSubject(subject_id=db_subject.id,student_id=db_student.id,note=note))

    
        db.add(db_subject)
        db.commit()
        db.refresh(db_subject)
        
    return db_subject


def delete_subject(subject_id: str, db: Session) -> models.Subject:
    db_subject = get_subject_by_id(subject_id=subject_id, db=db)

    for student in db_subject.students : 
        db.delete(student)
    db.commit()
    db.refresh(db_subject)
    db.delete(db_subject)
    db.commit()
    return db_subject


def delete_all_subjects(db: Session) -> List[models.Subject]:

    records = db.query(models.StudentSubject).filter()
    for record in records:
        db.delete(record)
    db.commit()

    records = db.query(models.Subject).filter()
    for record in records:
        db.delete(record)
    db.commit()
    return records