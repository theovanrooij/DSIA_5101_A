from typing import List, Optional
from datetime import date,datetime
from pydantic import BaseModel, Field
from uuid import uuid4
from typing_extensions import Annotated
# from .subjects import Subjects

class Students(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    family_name: str
    first_name: str
    birth_date: Annotated[date, Field(default_factory=lambda: datetime.now())]
    academic_level: str
    class_student: str
    created_at: Annotated[date, Field(default_factory=lambda: datetime.now())]
    updated_at: Annotated[date, Field(default_factory=lambda: datetime.now())]
    subjects: Optional[List] = []

    class Config:
        orm_mode = True
