from sqlalchemy import Column, String, Date,DateTime
from sqlalchemy.dialects.postgresql import UUID
from .database import BaseSQL


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
    
