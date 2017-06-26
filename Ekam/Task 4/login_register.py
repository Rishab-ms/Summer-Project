from flask import Flask , render_template , request
from flask_sqlalchemy import SQLAlchemy
import os
import hashlib
#Creating instance of Flask
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app_hashed.db')

db = SQLAlchemy(app)

# Creating Database
class User(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(100) , nullable = False)
    password = db.Column(db.String(200) , nullable  = False)

    def __init__(self , username , password):
        self.username = username
        self.password = password


#Creating the database
db.create_all()
db.session.commit()

# Defining app routes
@app.route('/')
def index():
    return render_template('index.html')

# User Login
@app.route('/login' , methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # Get POSTed database
        input_data = request.get_json()

        # Find user in Database . If found proceed for password check Else return Error
        user_data = User.query.filter_by(username = input_data['username']).first()

        if user_data == None:
            return render_template('login.html' , error= "Incorrect username or password")

        # Hashing entered password
        hash_object = hashlib.sha256()
        password_bytecode = input_data['password'].encode('utf-8')
        hash_object.update(password_bytecode)
        hashed_password = hash_object.digest()

        # Password check
        if user_data.password == hashed_password:
            return render_template('login.html', user = user_data)
        else:
            return render_template('login.html' , error = 'Incorrect username or password')
    # If method is GET , render login page
    else:
        return render_template('login.html')

# New User Registration
@app.route('/register' , methods = ['GET' , 'POST'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        input_data = request.get_json()

        if len(str(input_data['password'])) <8 or len(str(input_data['password'])) > 24:
            return render_template('register.html' , error = 'Password should be between 8 to 24 characters')
        if username_taken(input_data['username']):
            return render_template('register.html' , error = 'Username is not available')

        # Hashing Password
        hash_object = hashlib.sha256()
        password_bytecode = input_data['password'].encode('utf-8')
        hash_object.update(password_bytecode)
        hashed_password = hash_object.digest()

        # Adding to db
        new_registration = User(input_data['username'] , hashed_password )
        db.session.add(new_registration)
        db.session.commit()

        return render_template('register.html' , user = input_data)

# Check if username exists
def username_taken(input_username):
    name = User.query.filter_by(username = input_username).first()
    if name == None:
        return False
    else:
        return True

# Run CRUD
if __name__ == "__main__":
    app.run(debug = True)

