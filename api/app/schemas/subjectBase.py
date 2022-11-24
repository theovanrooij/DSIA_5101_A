from datetime import date,datetime
from pydantic import BaseModel, Field
from uuid import uuid4
from typing_extensions import Annotated
from typing import Optional

class SubjectBase(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex,alias="subject_id")] 
    code_subject: str = Field(alias="code_subject")
    name_subject: str = Field(alias="name_subject")
    created_at: Annotated[date, Field(default_factory=lambda: datetime.now(),alias="created_at")]
    updated_at: Annotated[date, Field(default_factory=lambda: datetime.now(),alias="updated_at")] 
    note: Optional[int]
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True