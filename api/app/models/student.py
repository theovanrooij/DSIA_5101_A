from sqlalchemy import Column, String, Date
from sqlalchemy.dialects.postgresql import UUID
from .database import BaseSQL


class Student(BaseSQL):
    __tablename__ = "student"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    first_name = Column(String)
    family_name = Column(String)
    birth_date = Column(Date())
    created_at = Column(Date())
    updated_at = Column(Date())
    
