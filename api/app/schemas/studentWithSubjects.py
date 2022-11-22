from typing import List,Optional
from .studentBase import StudentBase

class StudentWithSubjects(StudentBase):
    subjects: Optional[List]