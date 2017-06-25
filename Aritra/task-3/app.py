from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://crud:summer@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
class crud(db.Model):
	__tablename__='aTable'
	name=db.Column(db.String(64),unique=True,nullable=False)
	age=db.Column(db.Integer,nullable=False)
	username=db.Column(db.String(64),primary_key=True,nullable=False)
	password=db.Column(db.String(50),nullable=False)

db.create_all()
db.session.commit()
def isNone(a,b):
	if a is None or a=='':
		return b
	else:
		return a

@app.route('/')
def index():
	return "Should have made a base.html \_(-_-)_/"

@app.route('/create',methods=['GET','POST'])
def create():
	if request.method=='POST':
		data=request.form
		add=crud()
		add.name=data['name']
		add.age=int(data['age'])
		add.username=data['username']
		add.password=data['password']
		if db.session.query(crud).filter_by(username=data['username']).scalar() is not None:
			return render_template('create.html', message='could not create that username')
		if  db.session.query(crud).filter_by(name=data['name']).scalar() is not None:
			return render_template('create.html',message='you have already made an account with that name')
		db.session.add(add)
		db.session.commit()	
		return redirect('/')
	else:
		return render_template('create.html')

@app.route('/read',methods=['GET','POST'])
def read():
	if request.method=='POST':
		data=request.form
		x=db.session.query(crud).filter_by(username=data['username']).all()
		return render_template('read.html',values=x)
	else:
		return render_template('read.html',values=None)

@app.route('/update',methods=['GET','POST'])
def update():
	if request.method=='POST':
		data=request.form
		x=db.session.query(crud).filter_by(username=data['username']).first()
		if x is not None:
			x.name=isNone(data['name'],x.name)
			x.age=isNone(data['age'],x.age)
			db.session.add(x)
			db.session.commit()
			return 'Done!'
		else:
			return render_template('update.html',message="Username doesn't exist")
	else:
		return render_template('update.html')

@app.route('/delete',methods=['GET','POST'])
def delete():
	if request.method=='POST':
		data=request.form
		x=db.session.query(crud).filter_by(username=data['username']).first()
		if x is not None:
			db.session.delete(x)
			db.session.commit()
			return 'Done!'
		else:
			return render_template('delete.html',message="Username doesn't exist")
	else:
		return render_template('delete.html')

if __name__=='__main__':
	app.run(debug=True)