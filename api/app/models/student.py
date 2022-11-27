from sqlalchemy import Column, String, Date,DateTime,Table,ForeignKey,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship,backref
from .database import BaseSQL
from sqlalchemy.ext.associationproxy import association_proxy


class StudentSubject(BaseSQL):
    __tablename__ ='studentsubject'
    student_id = Column(ForeignKey('student.id',onupdate="CASCADE",ondelete="CASCADE"), primary_key=True)
    subject_id = Column(ForeignKey('subject.id',onupdate="CASCADE",ondelete="CASCADE"), primary_key=True)
    note = Column(Integer, nullable=True)
    student = relationship("Student", back_populates="subjects")
    subject = relationship("Subject", back_populates="students")

    family_name = association_proxy(target_collection='student', attr='family_name')
    first_name = association_proxy(target_collection='student', attr='first_name')
    birth_date = association_proxy(target_collection='student', attr='birth_date')
    academic_level = association_proxy(target_collection='student', attr='academic_level')
    class_student = association_proxy(target_collection='student', attr='class_student')
    created_at = association_proxy(target_collection='student', attr='created_at')
    updated_at = association_proxy(target_collection='student', attr='updated_at ')

    name_subject = association_proxy(target_collection='subject', attr='name_subject')
    code_subject = association_proxy(target_collection='subject', attr='code_subject')
    subject_created_at = association_proxy(target_collection='subject', attr='created_at')
    subject_updated_at = association_proxy(target_collection='subject', attr='updated_at')

class Student(BaseSQL):
    __tablename__ = "student"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    family_name = Column(String)
    first_name = Column(String)
    birth_date = Column(Date())
    academic_level = Column(String)
    class_student = Column(String)
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    subjects = relationship("StudentSubject", back_populates='student',cascade="all,delete")
