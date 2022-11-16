from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from .database import BaseSQL


class Subject(BaseSQL):
    __tablename__ = "subject"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    code_subject = Column(String)
    name_subject = Column(String)
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    
