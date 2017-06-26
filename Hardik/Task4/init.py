from flask import Flask, request, Response
import json
import hashlib
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:boltzman27@localhost/credentials'
db = SQLAlchemy(app)

class Mysql(db.Model):
    __tablename__='details'
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(128))

db.create_all()
db.session.commit()

@app.route('/login', methods=['POST'])
def login():
    username=request.json.get("username", "")
    password=request.json.get("password", "")
    status=signin(username, hashlib.md5(password.encode()).hexdigest())
    if not status:
        return Response('Invalid credentials', status=200)
    else:
        return Response('Login Successful', status=200)

@app.route('/register', methods=['POST'])
def register():
    username=request.json.get("username", "")
    password=request.json.get("password", "")
    status=validate(username, password)
    if status=='success':
        authorize(username, hashlib.md5(password.encode()).hexdigest())
        return Response('Credentials authorized', status=201)
    elif status=="duplicate":
        return Response('Duplicate credentials', status=200)
    else:
        return Response('Blank field', status=400)

def validate(username, password):
    if not username or not password:
        return 'blank'
    else:
        data = Mysql.query.filter_by(username=username).first()
        if data != None:
            return 'duplicate'
        else:
            return 'success'

def authorize(username, password_md5):
    data = Mysql(username=username, password=password_md5)
    db.session.add(data)
    db.session.commit()
    return

def signin(username, password_md5):
    data = Mysql.query.filter_by(username=username).first()
    if data != None:
        if data.password==password_md5:
            return 1
    return 0

if __name__=="main":
    app.run
