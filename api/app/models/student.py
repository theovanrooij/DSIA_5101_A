from sqlalchemy import Column, String, Date,DateTime,Table,ForeignKey,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship,backref
from .database import BaseSQL

from sqlalchemy.orm import relationship

StudentSubjectRelation = Table('studentsubjectrelation', BaseSQL.metadata,
    Column('student_id', UUID(as_uuid=True), ForeignKey('student.id',onupdate="CASCADE",ondelete="CASCADE")),
    Column('subject_id', UUID(as_uuid=True), ForeignKey('subject.id',onupdate="CASCADE",ondelete="CASCADE"))
)

class StudentSubject(BaseSQL):
    __tablename__ ='studentsubject'
    student_id = Column(ForeignKey('student.id'), primary_key=True)
    subjects_id = Column(ForeignKey('subject.id'), primary_key=True)
    note = Column(Integer, nullable=True)
    student = relationship("Student", back_populates="subjects")
    subject = relationship("Subject", back_populates="students")
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
    subjects = relationship("StudentSubject", back_populates='student')


    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

