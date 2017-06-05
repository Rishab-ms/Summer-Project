from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://shreyansh:@localhost/shreyansh'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)


#Homepage returning the type of http request method used to call the page
@app.route('/',methods=['GET','POST'])
def homepage():
    return "Request method used is %s" % request.method

#For creating a new record
@app.route('/create',methods=['POST'])
def create():
    title = request.form["title"]
    description = request.form["description"]
    task = Task(title=title, description = description)
    db.session.add(task)
    db.session.commit()
    return "Data added successfully"

#For returning the details of the person
@app.route('/read',methods=['POST','GET'])
def read():

    return render_template('view_task.html',)

if __name__ == '__main__':
    app.run(debug=True)