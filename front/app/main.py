
from flask import Flask,render_template,request,redirect,abort
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
    return render_template("students.html",students=response.json())


@app.route('/student/<studentID>')
def studentDetail(studentID):
    response  = requests.get(app.config['API_URL']+"/students/"+studentID)
    if response.status_code != 200 :
        abort(response.status_code)
    return render_template("student-detail.html",student=response.json())


@app.route('/add-student')
def addStudent():
    form = studentForm()
    all_subjects  = requests.get(app.config['API_URL']+"/subjects")
    
    if all_subjects.status_code == 200 : 
        all_subjects_data = all_subjects.json()
        subjectChoices = []
        for subject in all_subjects_data:
            subjectChoices.append((subject["id"],
            subject["code_subject"]+"-"+subject["name_subject"]))
        form.subjects.choices = subjectChoices
    else : 
        all_subjects_data = []
    return render_template("add-student.html",form=form, all_subjects=all_subjects_data)


@app.route('/add-student-api', methods= ['POST'])
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
    
    if response.status_code != 200 :
        abort(response.status_code)
        return redirect("/")
    return redirect("/students")


@app.route('/student/remove-subject/<studentID>/<subjectID>', methods= ['GET'])
def removeStudentSubject(studentID,subjectID):
    student =  requests.get(app.config['API_URL']+"/students/"+studentID)
    if student.status_code != 200 :
        abort(student.status_code)

    student = student.json()
    subjects = student.get("subjects")
    student["subjects"] = []
    for subject in subjects :
        if not subject.get("id") == subjectID :
            student["subjects"].append([subject["id"],subject["note"] if subject["note"] else -1])
    response  = requests.put(app.config['API_URL']+"/students/"+studentID,json=student)

    if response.status_code != 200 :
        abort(response.status_code)

    return redirect("/student/"+studentID)


@app.route('/delete-student/<studentID>', methods= ['GET'])
def deleteStudentApi(studentID):
    response  = requests.delete(app.config['API_URL']+"/students/"+studentID)
    # if response.status_code != 200 :
    #     abort(response.status_code)
    return redirect("/students")


@app.route('/edit-student/<studentID>', methods= ['GET'])
def updateStudent(studentID):
    response  = requests.get(app.config['API_URL']+"/students/"+studentID)
    if response.status_code != 200 :
        abort(response.status_code)
    student = response.json()
    all_subjects  = requests.get(app.config['API_URL']+"/subjects")
    studentObj = student.copy()
    studentSubjectID = []
    if studentObj["subjects"]:
        studentSubjectID = [subject["id"] for subject in studentObj["subjects"] ]
  
    if all_subjects.status_code == 200 : 
        all_subjects_data = all_subjects.json()
        subjectChoices = []
        subjectsID = []
        for subject in all_subjects_data:
            subjectChoices.append((subject["id"],
            subject["code_subject"]+"-"+subject["name_subject"]))
            if subject["id"] in studentSubjectID :
                subjectsID.append(subject["id"])
        studentObj["subjects"] = subjectsID
        
    else : 
        all_subjects_data = []
        subjectChoices = []
        subjectsID=()
    form = studentForm(obj=studentObj)
    form.subjects.choices = subjectChoices
    form.subjects.default = subjectsID
    form.process()
    
    return render_template("edit-student.html",form=form,obj=studentObj,student=student,all_subjects=all_subjects_data)


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

    response  = requests.put(app.config['API_URL']+"/students/"+studentID,json=new_student)

    if response.status_code != 200 :
        abort(response.status_code)
    return redirect("/students")


## Teachers 

@app.route('/teachers')
def teachers():
    response  = requests.get(app.config['API_URL']+"/teachers")
    if response.status_code != 200 :
        abort(response.status_code)
    return render_template("teachers.html",teachers=response.json())


@app.route('/teacher/<teacherID>')
def teacherDetail(teacherID):
    response  = requests.get(app.config['API_URL']+"/teachers/subjects/"+teacherID)
    if response.status_code != 200 :
        abort(response.status_code)
    return render_template("teacher-detail.html",teacher=response.json())


@app.route('/add-teacher')
def addTeacher():
    form = teacherForm()
    all_subjects  = requests.get(app.config['API_URL']+"/subjects")

    if all_subjects.status_code == 200 : 
        all_subjects_data = all_subjects.json()
        subjectChoices = []
        for subject in all_subjects_data:
            subjectChoices.append((subject["id"],
            subject["code_subject"]+"-"+subject["name_subject"]))
        form.subjects.choices = subjectChoices
    else : 
        all_subjects_data = []
    return render_template("add-teacher.html",form=form, all_subjects=all_subjects_data)


@app.route('/add-teacher-api', methods= ['POST','GET'])
def addTeacherApi():
    formData = request.form.to_dict(flat=False)
    new_teacher = dict()
    for var,value in formData.items() : 
        new_teacher[var] = value[0]
    new_teacher["subjects"] = formData.get("subjects")
    response  = requests.post(app.config['API_URL']+"/teachers",json=new_teacher)
    if response.status_code != 200 :
        abort(response.status_code)
    return redirect("/teachers")


@app.route('/teacher/remove-subject/<teacherID>/<subjectID>', methods= ['POST','GET'])
def removeTeacherSubject(teacherID,subjectID):
    # return "a"
    teacher =  requests.get(app.config['API_URL']+"/teachers/subjects/"+teacherID)
    if teacher.status_code != 200 :
        abort(teacher.status_code)
    teacher = teacher.json()
    subjects = teacher.get("subjects")
    teacher["subjects"] = []
    for subject in subjects :
        if not subject.get("id") == subjectID :
            teacher["subjects"].append(subject["id"])
    response  = requests.put(app.config['API_URL']+"/teachers/"+teacherID,json=teacher)
    if response.status_code != 200 :
        abort(response.status_code)
    return redirect("/teacher/"+teacherID)


@app.route('/delete-teacher/<teacherID>', methods= ['GET'])
def deleteTeacherApi(teacherID):
    response  = requests.delete(app.config['API_URL']+"/teachers/"+teacherID)
    # if response.status_code != 200 :
    #     abort(response.status_code)
    return redirect("/teachers")


@app.route('/edit-teacher/<teacherID>', methods= ['GET'])
def updateTeacher(teacherID):
    response  = requests.get(app.config['API_URL']+"/teachers/subjects/"+teacherID)
    if response.status_code != 200 :
        abort(response.status_code)
    teacher = response.json()
    all_subjects  = requests.get(app.config['API_URL']+"/subjects")

    teacherObj = teacher.copy()
    teacherSubjectID = []
    if teacherObj["subjects"]:
        teacherSubjectID = [subject["id"] for subject in teacherObj["subjects"] ]
  

    if all_subjects.status_code == 200 : 
        all_subjects_data = all_subjects.json()
        subjectChoices = []
        subjectsID = []
        for subject in all_subjects_data:
            subjectChoices.append((subject["id"],
            subject["code_subject"]+"-"+subject["name_subject"]))
            if subject["id"] in teacherSubjectID :
                subjectsID.append(subject["id"])
        teacherObj["subjects"] = subjectsID
        
    else : 
        all_subjects_data = []
        subjectChoices = []
        subjectsID=()
    form = teacherForm(obj=teacherObj)
    form.subjects.choices = subjectChoices
    form.subjects.default = subjectsID
    form.process()
    return render_template("edit-teacher.html",form=form,obj=teacherObj,teacher=teacher,all_subjects=all_subjects_data)


@app.route('/edit-teacher-api/<teacherID>', methods= ['POST','GET'])
def editTeacherApi(teacherID):
    formData = request.form.to_dict(flat=False)
    new_teacher = dict()
    for var,value in formData.items() : 
        new_teacher[var] = value[0]
    new_teacher["subjects"] = formData.get("subjects")
    new_teacher["id"] = teacherID
    response  = requests.put(app.config['API_URL']+"/teachers/"+teacherID,json=new_teacher)
    if response.status_code != 200 :
        abort(response.status_code)
    return redirect("/teachers")


## Mati??res/Unit??s

@app.route('/subjects')
def subjects():
    response  = requests.get(app.config['API_URL']+"/subjects")
    if response.status_code != 200 :
        abort(response.status_code)
    return render_template("subjects.html",subjects=response.json(),all_subjects=response.json())


@app.route('/subject/<subjectID>')
def subjectDetail(subjectID):
    
    response  = requests.get(app.config['API_URL']+"/subjects/"+subjectID)
    if response.status_code != 200 :
        abort(response.status_code)
    return render_template("subject-detail.html", subject=response.json())


@app.route('/add-subject')
def addSubject():
    form = subjectForm()
    return render_template("add-subject.html",form=form)


@app.route('/add-subject-api', methods= ['GET'])
def addSubjectApi():
    jsonDict = dict(request.args)
    response  = requests.post(app.config['API_URL']+"/subjects",json=jsonDict)
    if response.status_code != 200 :
        abort(response.status_code)
    return redirect("/subjects")


@app.route('/delete-subject/<subjectID>', methods= ['GET'])
def deleteSubjectApi(subjectID):
    response  = requests.delete(app.config['API_URL']+"/subjects/"+subjectID)
    # if response.status_code != 200 :
    #     abort(response.status_code)
    return redirect("/subjects")


@app.route('/edit-subject/<subjectID>', methods= ['GET'])
def updateSubject(subjectID):
    response  = requests.get(app.config['API_URL']+"/subjects/"+subjectID)
    if response.status_code != 200 :
        abort(response.status_code)
    subject = response.json()
    form = subjectForm(obj=subject)
    return render_template("edit-subject.html",form=form,subject=subject)


@app.route('/edit-subject-api/<subjectID>', methods= ['GET'])
def editSubjectApi(subjectID):
    formData = request.args.to_dict()
    new_subject = dict()
    for var,value in formData.items() : 
        new_subject[var] = value
    new_subject["id"] = subjectID
    response  = requests.put(app.config['API_URL']+"/subjects/"+subjectID,json=new_subject)
    if response.status_code != 200 :
        abort(response.status_code)
    return redirect("/subjects")


@app.route('/subjects/remove-teacher/<subjectID>/<teacherID>', methods= ['POST','GET'])
def removeSubjectTeacher(subjectID,teacherID):
    subject =  requests.get(app.config['API_URL']+"/subjects/"+subjectID)
    if subject.status_code != 200 :
        abort(subject.status_code)
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
    response  = requests.put(app.config['API_URL']+"/subjects/"+subjectID,json=subject)
    if response.status_code != 200 :
        abort(response.status_code)
    return redirect("/subject/"+subjectID)


@app.route('/subjects/remove-student/<subjectID>/<studentID>', methods= ['POST','GET'])
def removeSubjectStudent(subjectID,studentID):
    subject =  requests.get(app.config['API_URL']+"/subjects/"+subjectID)
    if subject.status_code != 200 :
        abort(subject.status_code)
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
    response  = requests.put(app.config['API_URL']+"/subjects/"+subjectID,json=subject)
    if response.status_code != 200 :
        abort(response.status_code)
    return redirect("/subject/"+subjectID)


def changeNote(subjectID,studentID,noteValue):
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
    return response


@app.route('/subjects/edit-note/<subjectID>/<studentID>/<noteValue>', methods= ['POST','GET'])
def editNoteSubject(subjectID,studentID,noteValue):
    response = changeNote(subjectID,studentID,noteValue)
    return redirect("/subject/"+subjectID)


@app.route('/students/edit-note/<subjectID>/<studentID>/<noteValue>', methods= ['POST','GET'])
def editNoteStudent(subjectID,studentID,noteValue):
    response = changeNote(subjectID,studentID,noteValue)
    return redirect("/student/"+studentID)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.errorhandler(409)
def ressource_exist(e):
    return render_template("409.html")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html")


if __name__ == '__main__':
    
    app.run(debug=True,host="0.0.0.0" ,port=8050)