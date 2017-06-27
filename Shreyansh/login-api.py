from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://shreyansh:@localhost/shreyansh'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'login_activity'

    username = db.Column(name='username', type_=db.VARCHAR, primary_key=True)
    password = db.Column(name='password', type_=db.VARCHAR)

@app.route('/')
def home():
    return 'Welcome to the login and registration api'

@app.route('/login/',methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.get(data["username"])
    if data["username"] == "":
        result = "Username field empty"
    elif data["password"] == "":
        result = "Password field empty"
    elif user == None:
        result = "Username not found"
    elif check_password_hash(user.password,data["password"]):
        result = "Successful login"
    else:
        result = "Incorrect Password"
    message = {"result":result}
    return jsonify(message)

@app.route('/register/',methods=["POST"])
def register():
    data = request.get_json()
    user = User.query.get(data["username"])
    if data["username"] == "":
        result = "Username field is empty"
    elif data["password"] == "":
        result = "Password field is empty"
    elif user != None:
        result = "Username already exists"
    else:
        user = User(username = data["username"],password = generate_password_hash(data["password"]))
        db.session.add(user)
        db.session.commit()
        result = "User created successfully"

    message = {"result":result}
    return jsonify(message)

if __name__ == '__main__':
    app.run(debug=True)