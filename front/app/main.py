
from flask import Flask,render_template,request,redirect
import requests
from forms import studentForm, teacherForm, subjectForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
app.config['API_URL'] = "http://api:5000"

@app.route('/')
def root():
    return render_template("accueil.html",text=requests.get(app.config['API_URL']).text)


## Students 

@app.route('/students')
def students():
    response  = requests.get(app.config['API_URL']+"/students")
    # return response.content

    return render_template("students.html",students=response.json())

@app.route('/student/<studentID>')
def studentDetail(studentID):
    response  = requests.get(app.config['API_URL']+"/students/"+studentID)
    return render_template("student-detail.html",student=response.json())


@app.route('/add-student')
def addStudent():

    form = studentForm()
    all_subjects  = requests.get(app.config['API_URL']+"/subjects")
    return render_template("add-student.html",form=form, all_subjects=all_subjects.json())

@app.route('/add-student-api', methods= ['POST','GET'])
def addStudentApi():

    formData = request.form.to_dict(flat=False)
    new_student = dict()
    for var,value in formData.items() : 
        new_student[var] = value[0]
    new_student["subjects"] = []
    subjects=formData.get("subjects")
    if subjects :
        for subject in  subjects: 
            new_student["subjects"].append([subject,-1])
    response  = requests.post(app.config['API_URL']+"/students",json=new_student)
    return redirect("/students")

@app.route('/student/remove-subject/<studentID>/<subjectID>', methods= ['POST','GET'])
def removeStudentSubject(studentID,subjectID):

    student =  requests.get(app.config['API_URL']+"/students/"+studentID).json()
    # return student
    subjects = student.get("subjects")
    student["subjects"] = []
    for subject in subjects :
        if not subject.get("id") == subjectID :
            student["subjects"].append([subject["id"],subject["note"] if subject["note"] else -1])
    response  = requests.put(app.config['API_URL']+"/students/"+studentID,json=student)
    return redirect("/student/"+studentID)



@app.route('/delete-student/<studentID>', methods= ['GET'])
def deleteStudentApi(studentID):

    response  = requests.delete(app.config['API_URL']+"/students/"+studentID)
    return redirect("/students")

@app.route('/edit-student/<studentID>', methods= ['GET'])
def updateStudent(studentID):
    response  = requests.get(app.config['API_URL']+"/students/"+studentID)
    student = response.json()
    all_subjects  = requests.get(app.config['API_URL']+"/subjects")
    form = studentForm(obj=student)
    return render_template("edit-student.html",form=form,student=student,all_subjects=all_subjects.json())

@app.route('/edit-student-api/<studentID>', methods= ['POST','GET'])
def editStudentApi(studentID):
    formData = request.form.to_dict(flat=False)
    new_student = dict()
    for var,value in formData.items() : 
        new_student[var] = value[0]
    new_subjects = list()

    subjectsForm = formData.get("subjects")
    if subjectsForm :
        for subject in  subjectsForm: 
            new_subjects.append([subject,-1])
        new_student["subjects"] = new_subjects if new_subjects else []
    new_student["id"] = studentID
    # return new_student
    response  = requests.put(app.config['API_URL']+"/students/"+studentID,json=new_student)
    # return response.content
    return redirect("/students")


## Teachers 

@app.route('/teachers')
def teachers():
    response  = requests.get(app.config['API_URL']+"/teachers")
    return render_template("teachers.html",teachers=response.json())

@app.route('/teacher/<teacherID>')
def teacherDetail(teacherID):
    response  = requests.get(app.config['API_URL']+"/teachers/subjects/"+teacherID)
    return render_template("teacher-detail.html",teacher=response.json())


@app.route('/add-teacher')
def addTeacher():

    form = teacherForm()
    all_subjects  = requests.get(app.config['API_URL']+"/subjects")
    return render_template("add-teacher.html",form=form, all_subjects=all_subjects.json())

@app.route('/add-teacher-api', methods= ['POST','GET'])
def addTeacherApi():

    formData = request.form.to_dict(flat=False)
    new_teacher = dict()
    for var,value in formData.items() : 
        new_teacher[var] = value[0]
    new_teacher["subjects"] = formData.get("subjects")

    response  = requests.post(app.config['API_URL']+"/teachers",json=new_teacher)
    return redirect("/teachers")


@app.route('/teacher/remove-subject/<teacherID>/<subjectID>', methods= ['POST','GET'])
def removeTeacherSubject(teacherID,subjectID):

    teacher =  requests.get(app.config['API_URL']+"/teachers/subjects/"+teacherID).json()

    subjects = teacher.get("subjects")
    teacher["subjects"] = []
    for subject in subjects :
        if not subject.get("id") == subjectID :
            teacher["subjects"].append(subject["id"])
    response  = requests.put(app.config['API_URL']+"/teachers/"+teacherID,json=teacher)
    return redirect("/teacher/"+teacherID)



@app.route('/delete-teacher/<teacherID>', methods= ['GET'])
def deleteTeacherApi(teacherID):

    response  = requests.delete(app.config['API_URL']+"/teachers/"+teacherID)
    return redirect("/teachers")


@app.route('/edit-teacher/<teacherID>', methods= ['GET'])
def updateTeacher(teacherID):

    response  = requests.get(app.config['API_URL']+"/teachers/"+teacherID)
    teacher = response.json()
    all_subjects  = requests.get(app.config['API_URL']+"/subjects")
    form = teacherForm(obj=teacher)
    return render_template("edit-teacher.html",form=form,teacher=teacher,all_subjects=all_subjects.json())

@app.route('/edit-teacher-api/<teacherID>', methods= ['POST','GET'])
def editTeacherApi(teacherID):
    
    formData = request.form.to_dict(flat=False)
    new_teacher = dict()
    for var,value in formData.items() : 
        new_teacher[var] = value[0]
    new_teacher["subjects"] = formData.get("subjects")
    new_teacher["id"] = teacherID
    response  = requests.put(app.config['API_URL']+"/teachers/"+teacherID,json=new_teacher)
    return redirect("/teachers")


## Matières/Unités

@app.route('/subjects')
def subjects():
    response  = requests.get(app.config['API_URL']+"/subjects")
    return render_template("subjects.html",subjects=response.json(),all_subjects=response.json())


@app.route('/subject/<subjectID>')
def subjectDetail(subjectID):
    students  = requests.get(app.config['API_URL']+"/subjects/students/"+subjectID)
    teachers = requests.get(app.config['API_URL']+"/subjects/teachers/"+subjectID)
    response  = requests.get(app.config['API_URL']+"/subjects/"+subjectID)
    # return students.json()
    return render_template("subject-detail.html", subject=response.json(),students=students.json(), teachers=teachers.json())

@app.route('/add-subject')
def addSubject():
    form = subjectForm()
    return render_template("add-subject.html",form=form)

@app.route('/add-subject-api', methods= ['GET'])
def addSubjectApi():
    jsonDict = dict(request.args)
    response  = requests.post(app.config['API_URL']+"/subjects",json=jsonDict)

    return redirect("/subjects")

@app.route('/delete-subject/<subjectID>', methods= ['GET'])
def deleteSubjectApi(subjectID):
    response  = requests.delete(app.config['API_URL']+"/subjects/"+subjectID)
    return redirect("/subjects")

@app.route('/edit-subject/<subjectID>', methods= ['GET'])
def updateSubject(subjectID):
    response  = requests.get(app.config['API_URL']+"/subjects/"+subjectID)
    subject = response.json()
    form = subjectForm(obj=subject)
    return render_template("edit-subject.html",form=form,subject=subject)

@app.route('/edit-subject-api/<subjectID>', methods= ['GET'])
def editSubjectApi(subjectID):
    # return request.args
    formData = request.args.to_dict()
    new_subject = dict()
    for var,value in formData.items() : 
        new_subject[var] = value
    new_subject["id"] = subjectID
    response  = requests.put(app.config['API_URL']+"/subjects/"+subjectID,json=new_subject)
    return redirect("/subjects")

@app.route('/subjects/remove-teacher/<subjectID>/<teacherID>', methods= ['POST','GET'])
def removeSubjectTeacher(subjectID,teacherID):

    subject =  requests.get(app.config['API_URL']+"/subjects/"+subjectID)
    # return teacherID
    subject = subject.json()
    teachers = subject.get("teachers")
    subject["teachers"] = []
    if teachers :
        for teacher in teachers :
            if not teacher.get("id") == teacherID :
                subject["teachers"].append(teacher["id"])

    students = subject.get("students")
    subject["students"] = []
    if students :
        for student in students :
            note = student["note"]
            if not note : 
                note=-1
            subject["students"].append([student["id"],note])
    # return subject
    response  = requests.put(app.config['API_URL']+"/subjects/"+subjectID,json=subject)
    # return response.content
    return redirect("/subject/"+subjectID)

@app.route('/subjects/remove-student/<subjectID>/<studentID>', methods= ['POST','GET'])
def removeSubjectStudent(subjectID,studentID):

    subject =  requests.get(app.config['API_URL']+"/subjects/"+subjectID)
    subject = subject.json()
    teachers = subject.get("teachers")
    subject["teachers"] = []
    if teachers :
        for teacher in teachers :
            subject["teachers"].append(teacher["id"])

    students = subject.get("students")
    subject["students"] = []
    for student in students :
        if not student.get("id") == studentID :
            note = student["note"]
            if not note : 
                note=-1
            subject["students"].append([student["id"],note])
    # return subject
    response  = requests.put(app.config['API_URL']+"/subjects/"+subjectID,json=subject)
    # return response.content
    return redirect("/subject/"+subjectID)


@app.route('/subjects/edit-note/<subjectID>/<studentID>/<noteValue>', methods= ['POST','GET'])
def editNoteSubject(subjectID,studentID,noteValue):

    subject =  requests.get(app.config['API_URL']+"/subjects/"+subjectID)
    subject = subject.json()
    teachers = subject.get("teachers")
    subject["teachers"] = []
    if teachers :
        for teacher in teachers :
            subject["teachers"].append(teacher["id"])

    students = subject.get("students")
    subject["students"] = []

    for student in students :
        if not student.get("id") == studentID :
            note = student["note"]
            if not note : 
                note=-1
            subject["students"].append([student["id"],note])
        else :
            subject["students"].append([student["id"],int(noteValue)])
    response  = requests.put(app.config['API_URL']+"/subjects/"+subjectID,json=subject)
    return redirect("/subject/"+subjectID)

@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")



if __name__ == '__main__':
    
    app.run(debug=True,host="0.0.0.0" ,port=8050)