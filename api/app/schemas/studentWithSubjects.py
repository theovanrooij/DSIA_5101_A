from typing import List,Optional
from .studentBase import StudentBase
from .subjectBase import SubjectBase
class StudentWithSubjects(StudentBase):
    subjects: Optional[List[SubjectBase]]