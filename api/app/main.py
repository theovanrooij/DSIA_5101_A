import datetime
from fastapi import FastAPI
from models import engine,BaseSQL
import routers

app = FastAPI(
    title="My title",
    description="My description",
    version="0.0.1",
)
app.include_router(routers.HealthRouter)
app.include_router(routers.StudentRouter)
app.include_router(routers.TeacherRouter)
app.include_router(routers.SubjectRouter)

@app.on_event("startup")
async def startup_event():
    BaseSQL.metadata.create_all(bind=engine)
    
@app.get("/")
def read_root():
    return {"Hello": "World API"}

@app.get("/add-student")
def addStudent():
    return {"Student": "World API"}

@app.get("/add-teacher")
def addTeacher():
    return {"Teacher": "World API"}

@app.get("/add-subject")
def addSubject():
    return {"Subject": "World API"}


@app.get("/add-subject-student")
def addSubjectStudent():

    import schemas

    return {"Subject": "World API"}

@app.get("/add-subject-teacher")
def addSubjectTeacher():

    import schemas

    return {"Subject": "World API"}


@app.get("/date")
def read_root():
    return {"Date": datetime.datetime.today()}