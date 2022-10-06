from sqlalchemy import Column, String, Date,DateTime
from sqlalchemy.dialects.postgresql import UUID
from .database import BaseSQL


class Unite(BaseSQL):
    __tablename__ = "unité"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    Code_unite = Column(String)
    Name_unite = Column(String)
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    
