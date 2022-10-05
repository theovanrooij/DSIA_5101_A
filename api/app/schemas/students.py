from typing import List, Optional
from datetime import date,datetime
from pydantic import BaseModel, Field
from uuid import uuid4
from typing_extensions import Annotated


class Students(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    first_name: str
    family_name: str
    birth_date: Annotated[date, Field(default_factory=lambda: datetime.now())]
    created_at: Annotated[date, Field(default_factory=lambda: datetime.now())]
    updated_at: Annotated[date, Field(default_factory=lambda: datetime.now())]

    class Config:
        orm_mode = True
