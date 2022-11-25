from typing import List,Optional,Tuple
from .studentBase import StudentBase
from .subjectBase import SubjectBase
class StudentWithSubjects(StudentBase):
    subjects: Optional[List[SubjectBase]]

    
class StudentInsert(StudentBase):
    subjects: Optional[List[Tuple[str,int]]]