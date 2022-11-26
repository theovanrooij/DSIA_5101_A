from datetime import date,datetime
from pydantic import BaseModel, Field
from uuid import uuid4
from typing_extensions import Annotated
from typing import Optional

class StudentBase(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex,alias="student_id")]
    family_name: str = Field(alias="student_family_name")
    first_name: str = Field(alias="first_name")
    birth_date: Annotated[date, Field(default_factory=lambda: datetime.now(),alias="birth_date")]
    academic_level: str= Field(alias="academic_level")
    class_student: str= Field(alias="class_student")
    created_at: Annotated[date, Field(default_factory=lambda: datetime.now(),alias="created_at")]
    updated_at: Annotated[date, Field(default_factory=lambda: datetime.now(),alias="updated_at")]
    note: Optional[int]
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


