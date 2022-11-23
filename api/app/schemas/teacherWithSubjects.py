from typing import List,Optional
from .teacherBase import TeacherBase

class TeacherWithSubjects(TeacherBase):
    subjects: Optional[List]