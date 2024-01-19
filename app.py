from flask import Flask, render_template
import json

app = Flask(__name__)

data = { "users" : [
    {
    "Name" : "Hasan Iqbal",
    "Age": "35",
    "Email" : "iqbal@global.com",
    "Phone": "215-226-5465"
    },
    {
    "Name" : "John Doe",
    "Age": "35",
    "Email" : "iqbal@global.com",
    "Phone": "215-226-5465"
    },
    {
    "Name" : "Jane doe",
    "Age": "35",
    "Email" : "iqbal@global.com",
    "Phone": "215-226-5465"
    }
]    
}

@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello Hasan")

@app.route("/Profile", methods=["POST", "GET"])
def Hasan():
    return json.dumps(data)

@app.route("/Account")
def Account():
    return "Account Endpoint"