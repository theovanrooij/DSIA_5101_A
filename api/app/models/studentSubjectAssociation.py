# from sqlalchemy import Column,Integer
# from sqlalchemy.dialects.postgresql import UUID
# from .database import BaseSQL
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import relationship

# class StudentSubjectAssociation(BaseSQL):
#     __tablename__ = "association_table"
#     student_id = Column(ForeignKey("student.id"), primary_key=True)
#     subject_id = Column(ForeignKey("subject.id"), primary_key=True)
#     note = Column(Integer)