
from flask import Flask,render_template,request,redirect
import requests
from forms import studentForm

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
    string  =  request.args.get('first_name') +request.args.get('family_name')  + request.args.get('birth_date')

    # return request.args

    response  = requests.post(app.config['API_URL']+"/students",json=request.args)
    return redirect("/students")

@app.route('/delete-student/<studentID>', methods= ['GET'])
def deleteStudentApi(studentID):

    response  = requests.delete(app.config['API_URL']+"/students/"+studentID)
    return redirect("/students")

@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")

if __name__ == '__main__':
    
    app.run(debug=True,host="0.0.0.0" ,port=8050)