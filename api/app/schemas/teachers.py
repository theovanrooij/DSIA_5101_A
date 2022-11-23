from typing import List, Optional
from datetime import date,datetime
from pydantic import BaseModel, Field
from uuid import uuid4
from typing_extensions import Annotated


class Teacher(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    family_name_teacher: str
    first_name_teacher: str
    birth_date_teacher: Annotated[date, Field(default_factory=lambda: datetime.now())]
    created_at: Annotated[date, Field(default_factory=lambda: datetime.now())]
    updated_at: Annotated[date, Field(default_factory=lambda: datetime.now())]

    class Config:
        orm_mode = True
