from sqlalchemy import Column, String, Date,DateTime,Table,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship,backref
from .database import BaseSQL

from sqlalchemy.orm import relationship

StudentSubjectRelation = Table('studentsubjectrelation', BaseSQL.metadata,
    Column('student_id', UUID(as_uuid=True), ForeignKey('student.id')),
    Column('subject_id', UUID(as_uuid=True), ForeignKey('subject.id'))
)
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
    # subjects = relationship("Subject",secondary=StudentSubjectRelation,backref=backref('students', lazy='dynamic'), lazy='dynamic',cascade="all, delete")


