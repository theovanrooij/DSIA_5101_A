from typing import List,Optional
from .subjectBase import SubjectBase

class SubjectWithStudents(SubjectBase):
    students: Optional[List]