import datetime
from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
import models,schemas
import routers

app = FastAPI(
    title="FullStack Data",
    description="My description",
    version="0.0.1",
)
app.include_router(routers.HealthRouter)
app.include_router(routers.StudentRouter)
app.include_router(routers.TeacherRouter)
app.include_router(routers.SubjectRouter)


@app.on_event("startup")
async def startup_event():
    models.BaseSQL.metadata.create_all(bind=models.engine)
    try:
        populate()
    except:
        print("failed to populate")
        pass
    

@app.get("/")
def read_root():
    return {"Hello": "World API"}


@app.get("/date")
def read_date():
    return {"Date": datetime.datetime.today()}


@app.get("/populate")
def populate():
    student1 =models.Student(id="ca3ec6429ea348aabba76064989f53d8",family_name="Nom_1",first_name="Prenom_1",birth_date = "2000-01-01",
    academic_level="E5",class_student="DSIA",
    created_at = datetime.datetime.now(),updated_at = datetime.datetime.now())

    student2 = models.Student(id="82d967e33543419eb7d7cb732a73358e",family_name="Nom_2",first_name="Prenom_2",birth_date = "2000-01-01",
    academic_level="E5",class_student="DSIA",
    created_at = datetime.datetime.now(),updated_at = datetime.datetime.now())

    student3 =models.Student(id="9affa894306d49048fe42ab3a793faf3",family_name="Nom_3",first_name="Prenom_3",birth_date = "2000-01-01",
    academic_level="E5",class_student="DSIA",
    created_at = datetime.datetime.now(),updated_at = datetime.datetime.now())

    student4 =models.Student(id="ae0a2ce5452344149d1fe6d2cf039a14",family_name="Nom_4",first_name="Prenom_4",birth_date = "2000-01-01",
    academic_level="E5",class_student="DSIA",
    created_at = datetime.datetime.now(),updated_at = datetime.datetime.now())
    
    teacher1 = models.Teacher(id="ae0a2ce5452344149d1fe6d2cf039a11",family_name="Nom_1",first_name="Prenom_1",birth_date = "1995-01-01",
    created_at = datetime.datetime.now(),updated_at = datetime.datetime.now())

    teacher2 = models.Teacher(id="ae0a2ce5452344149d1fe6d2cf039a12",family_name="Nom_2",first_name="Prenom_2",birth_date = "1995-01-01",
    created_at = datetime.datetime.now(),updated_at = datetime.datetime.now())

    subject1 = models.Subject(id="ae0a2ce5452344149d1fe6d2cf039a19",code_subject="DSIA-5101A",name_subject="Full Stack Data",
    created_at = datetime.datetime.now(),updated_at = datetime.datetime.now(),teachers=[teacher1])
    subject2 = models.Subject(id="ae0a2ce5452344149d1fe6d2cf039a62",code_subject="DSIA-5101B",name_subject="Full Stack Web",
    created_at = datetime.datetime.now(),updated_at = datetime.datetime.now(),teachers=[teacher1,teacher2])
    subject3 = models.Subject(id="ae0a2ce5452344149d1fe6d2cf039a32",code_subject="DSIA-5101C",name_subject="Data Engineering",
    created_at = datetime.datetime.now(),updated_at = datetime.datetime.now())

    studentSubjectRelation1 = models.StudentSubject(student_id=student1.id,subject_id=subject1.id,note=5)
    studentSubjectRelation2 = models.StudentSubject(student_id=student2.id,subject_id=subject1.id,note=None)
    studentSubjectRelation3 = models.StudentSubject(student_id=student3.id,subject_id=subject1.id,note=15)
    studentSubjectRelation4 = models.StudentSubject(student_id=student4.id,subject_id=subject1.id,note=10)
    studentSubjectRelation5 = models.StudentSubject(student_id=student1.id,subject_id=subject2.id,note=None)

    db = next(models.get_db())
    db.add_all([student1,student2,student3,student4,teacher1,teacher2,subject1,subject2,subject3,studentSubjectRelation1,
                    studentSubjectRelation2,studentSubjectRelation3,studentSubjectRelation4,studentSubjectRelation5])
    db.commit()
    return db
    