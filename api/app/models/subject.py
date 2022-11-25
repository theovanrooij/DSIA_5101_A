from sqlalchemy import Column, String, Date,DateTime,Table,ForeignKey,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship,backref
from .database import BaseSQL
from .student import StudentSubjectRelation
from .teacher import TeacherSubjectRelation


SubjectStudentRelation = Table('subjectstudentrelation', BaseSQL.metadata,
    Column('subject_id', UUID(as_uuid=True), ForeignKey('subject.id',onupdate="CASCADE",ondelete="CASCADE")),
    Column('student_id', UUID(as_uuid=True), ForeignKey('student.id',onupdate="CASCADE",ondelete="CASCADE"))
)

SubjectTeacherRelation = Table('subjectteacherrelation', BaseSQL.metadata,
    Column('subject_id', UUID(as_uuid=True), ForeignKey('subject.id',onupdate="CASCADE",ondelete="CASCADE")),
    Column('teacher_id', UUID(as_uuid=True), ForeignKey('teacher.id',onupdate="CASCADE",ondelete="CASCADE"))
)


class Subject(BaseSQL):
    __tablename__ = "subject"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    code_subject = Column(String)
    name_subject = Column(String)
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    students = relationship("Student", secondary="studentsubjectrelation", back_populates='subjects')
    teachers = relationship("Teacher", secondary="teachersubjectrelation", back_populates='subjects')
    students_sub = relationship("Student", secondary="subjectstudentrelation", back_populates='subjects_stu')
    teachers_sub = relationship("Teacher", secondary="subjectteacherrelation", back_populates='subjects_tea')

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

