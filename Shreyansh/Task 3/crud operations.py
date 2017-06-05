from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://shreyansh:@localhost/shreyansh'
db = SQLAlchemy(app)

class Task(db.Model):
    __tablename__ = 'task'

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

#For returning list of tasks
@app.route('/read',methods=['GET'])
def read():
    task = Task.query.all()
    return render_template('view_task.html',tasks = task)

#For editing a task
@app.route('/update',methods=['POST'])
def update():
    id = request.form["id"]
    task = Task.query.get(id)
    if task == None:
        return 'Task not found'
    task.title = request.form["title"]
    task.description = request.form["description"]
    db.session.commit()
    return "Task updated successfully"

#For deleting a task
@app.route('/delete',methods=['POST'])
def delete():
    id = request.form["id"]
    task = Task.query.get(id)
    if task == None:
        return 'Task not found'
    db.session.delete(task)
    db.session.commit()
    return "Task deleted successfully"

if __name__ == '__main__':
    app.run(debug=True)