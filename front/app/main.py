
from flask import Flask
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'

@app.route('/')
def root():
    return "Hello world \n"+requests.get("http://api:5000").text

if __name__ == '__main__':
    
    app.run(debug=True,host="0.0.0.0" ,port=8050) 