from sqlalchemy import Column, String, Date,DateTime,Table,ForeignKey,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship,backref
from .database import BaseSQL

from sqlalchemy.orm import relationship

TeacherSubjectRelation = Table('teachersubjectrelation', BaseSQL.metadata,
    Column('teacher_id', UUID(as_uuid=True), ForeignKey('teacher.id',onupdate="CASCADE",ondelete="CASCADE")),
    Column('subject_id', UUID(as_uuid=True), ForeignKey('subject.id',onupdate="CASCADE",ondelete="CASCADE"))
)

class Teacher(BaseSQL):
    __tablename__ = "teacher"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    family_name_teacher = Column(String)
    first_name_teacher = Column(String)
    birth_date_teacher = Column(Date())
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    subjects = relationship("Subject", secondary="teachersubjectrelation", back_populates='teachers')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
