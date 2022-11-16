from sqlalchemy import Column,Integer
from sqlalchemy.dialects.postgresql import UUID
from .database import BaseSQL
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Association(BaseSQL):
    __tablename__ = "association_table"
    left_id = Column(ForeignKey("student.id"), primary_key=True)
    right_id = Column(ForeignKey("subject.id"), primary_key=True)
    note = Column(Integer)
    subject = relationship("Subject")
    student = relationship("Student")