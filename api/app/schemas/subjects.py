from typing import List, Optional
from datetime import date,datetime
from pydantic import BaseModel, Field
from uuid import uuid4
from typing_extensions import Annotated
# from .students import Students

class Subjects(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    code_subject: str
    name_subject: str
    created_at: Annotated[date, Field(default_factory=lambda: datetime.now())]
    updated_at: Annotated[date, Field(default_factory=lambda: datetime.now())]
    students: Optional[List]

    class Config:
        orm_mode = True
