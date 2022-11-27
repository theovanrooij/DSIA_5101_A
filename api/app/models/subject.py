from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship,backref
from .database import BaseSQL
from .teacher import TeacherSubjectRelation


class Subject(BaseSQL):
    __tablename__ = "subject"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    code_subject = Column(String)
    name_subject = Column(String)
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    students = relationship("StudentSubject", back_populates='subject')
    teachers = relationship("Teacher", secondary="teachersubjectrelation", back_populates='subjects',cascade="all,delete")

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
