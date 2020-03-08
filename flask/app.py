from flask import Flask
from flask import render_template ,jsonify,request
import subprocess

#html5 localstorage  :  
app = Flask(__name__)

@app.route("/")
def index():
    title ='Which book should you read next ?'
    return render_template('index.html',title=title)

@app.route("/data")
def data():
    return ("mydata { 'key' : 'name' ,'values' :['megha']")

@app.route("/echo", methods =['POST'])
def echo():
    command =request.form['text']
    subprocess.call(['say', command])
    return index()

if __name__ == "__main__":
    app.run()


#http://127.0.0.1:5000/ 
#set FLASK_ENV=development