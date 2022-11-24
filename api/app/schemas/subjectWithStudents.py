from typing import List,Optional
from .subjectBase import SubjectBase
from .studentBase import StudentBase
class SubjectWithStudents(SubjectBase):
    students: Optional[List[StudentBase]]