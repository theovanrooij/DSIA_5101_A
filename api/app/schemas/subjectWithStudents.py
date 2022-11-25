from typing import List,Optional,Tuple
from .subjectBase import SubjectBase
from .studentBase import StudentBase
class SubjectWithStudents(SubjectBase):
    students: Optional[List[StudentBase]]


class SubjectInsert(SubjectBase):
    students: Optional[List[Tuple[str,int]]]