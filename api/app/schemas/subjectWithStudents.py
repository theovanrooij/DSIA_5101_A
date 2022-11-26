from typing import List,Optional,Tuple
from .subjectBase import SubjectBase
from .studentBase import StudentBase
from .teacherBase import TeacherBase
class SubjectWithStudents(SubjectBase):
    students: Optional[List[StudentBase]]
    teachers: Optional[List[TeacherBase]]
    
class SubjectInsert(SubjectBase):
    students: Optional[List[Tuple[str,int]]]
    teachers: Optional[List[Tuple[str]]]