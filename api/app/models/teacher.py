from sqlalchemy import Column, String, Date,DateTime
from sqlalchemy.dialects.postgresql import UUID
from .database import BaseSQL


class Teacher(BaseSQL):
    __tablename__ = "teacher"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    family_name_teacher = Column(String)
    first_name_teacher = Column(String)
    birth_date_teacher = Column(Date())
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    
