from flask import Flask , render_template , request
from flask_sqlalchemy import SQLAlchemy
import os
#Creating instance of Flask
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

db = SQLAlchemy(app)

# Creating Database
class User(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(100) , nullable = False)
    email = db.Column(db.String(100) , nullable = True)

    def __init__(self, name , email):
        self.name = name
        self.email = email


#Creating the database
db.create_all()
db.session.commit()

# Defining app routes
@app.route('/',methods=['GET','POST'])
def home():
    return render_template('base.html')
@app.route('/create' , methods = ['POST'])
def create():
    rec_data = request.get_json()
    new_user = User(rec_data['name'] , rec_data['email'])
    db.session.add(new_user)
    db.session.commit()
    return render_template('base.html')
@app.route('/read', methods = ['POST'])
def read():
    uid = request.get_json()
    id_to_read = uid['read_id']
    user_data = User.query.filter( User.id == id_to_read).first()
    return render_template('base.html')

@app.route('/delete', methods = ['POST'])
def delete():
    uid = request.get_json()
    to_delete = User.query.filter_by( id =uid['id']).first()
    db.session.delete(to_delete)
    db.session.commit()
    return render_template('base.html')
@app.route('/update', methods = ['POST'])
def update():
    update_data = request.get_json()
    update_id = update_data['id']
    old_data = User.query.filter_by( id == update_id).first()
    old_data['name'] = update_data['name']
    old_data['email'] = update_data['email']
    db.session.commit()
    return render_template('base.html')
# Run CRUD
if __name__ == "__main__":
    app.run(debug = True)   
