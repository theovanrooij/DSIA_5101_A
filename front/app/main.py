
from flask import Flask,render_template,request,redirect
import requests
from forms import studentForm, teacherForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
app.config['API_URL'] = "http://api:5000"

@app.route('/')
def root():
    return render_template("accueil.html",text=requests.get(app.config['API_URL']).text)

@app.route('/students')
def students():
    response  = requests.get(app.config['API_URL']+"/students")
    # return response.content

    return render_template("students.html",students=response.json())

@app.route('/add-student')
def addStudent():
    form = studentForm()
    return render_template("add-student.html",form=form)

@app.route('/add-student-api', methods= ['GET'])
def addStudentApi():
    response  = requests.post(app.config['API_URL']+"/students",json=request.args)
    return redirect("/students")

@app.route('/delete-student/<studentID>', methods= ['GET'])
def deleteStudentApi(studentID):

    response  = requests.delete(app.config['API_URL']+"/students/"+studentID)
    return redirect("/students")

@app.route('/edit-student/<studentID>', methods= ['GET'])
def updateStudent(studentID):

    response  = requests.get(app.config['API_URL']+"/students",json={"id":studentID})
    student = response.json()[0]
    # return student
    form = studentForm(obj=student)
    return render_template("edit-student.html",form=form,student=student)

@app.route('/edit-student-api/<studentID>', methods= ['GET'])
def editStudentApi(studentID):
    response  = requests.put(app.config['API_URL']+"/students/"+studentID,json=request.args)
    return redirect("/students")


@app.route('/teachers')
def teachers():
    response  = requests.get(app.config['API_URL']+"/teachers")
    # return response.content

    return render_template("teachers.html",teachers=response.json())

@app.route('/add-teacher')
def addTeacher():
    form = teacherForm()
    return render_template("add-teacher.html",form=form)

@app.route('/add-teacher-api', methods= ['GET'])
def addTeacherApi():
    response  = requests.post(app.config['API_URL']+"/teachers",json=request.args)
    return redirect("/teachers")

@app.route('/delete-teacher/<teacherID>', methods= ['GET'])
def deleteTeacherApi(studentID):

    response  = requests.delete(app.config['API_URL']+"/teachers/"+studentID)
    return redirect("/teachers")

@app.route('/edit-teacher/<teacherID>', methods= ['GET'])
def updateTeacher(teacherID):

    response  = requests.get(app.config['API_URL']+"/teachers",json={"id":teacherID})
    teacher = response.json()[0]
    form = teacherForm(obj=teacher)
    return render_template("edit-teacher.html",form=form,teacher=teacher)

@app.route('/edit-teacher-api/<teacherID>', methods= ['GET'])
def editTeacherApi(teacherID):
    response  = requests.put(app.config['API_URL']+"/teachers/"+teacherID,json=request.args)
    return redirect("/teachers")


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")

if __name__ == '__main__':
    
    app.run(debug=True,host="0.0.0.0" ,port=8050)