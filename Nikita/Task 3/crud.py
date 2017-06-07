
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__, template_folder = 'templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Color(db.Model):
	__tablename__ = 'color'

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(80))
	fav_color = db.Column(db.String(80))

db.create_all()
db.session.commit()

@app.route('/', methods = ['GET', 'POST'])
def colors():
	return render_template('/colors.html')


@app.route('/create', methods = ['POST', 'GET'])
def create():
	if request.method == "GET":
		return render_template('/create.html')
	if request.method == "POST":
		name = request.form['name']
		fav_color = request.form['col']
		data = Color(name = name, fav_color = fav_color)
		db.session.add(data)
		db.session.commit()
		return render_template('/submission.html')


@app.route('/read', methods = ['GET', 'POST'])
def read():
	if request.method == "GET":
		fields = Color.query.all()
		return render_template('/read.html', fields = fields)


@app.route('/update', methods = ['GET', 'POST'])
def update():
	if request.method == "GET":
		return render_template('/update.html')
	if request.method == "POST":
		name = request.form['name']
		fav = request.form['fav']
		field = Color.query.filter_by(name = name).first()
		field.fav_color = fav
		db.session.commit()
		return render_template('/submission.html')

@app.route('/delete', methods = ['GET', 'POST'])
def delete():
	if request.method == "GET":
		return render_template('/delete.html')
	if request.method == "POST":
		name = request.form['name']
		field = Color.query.filter_by(name = name).first()
		db.session.delete(field)
		db.session.commit()
		return render_template('/submission.html')


if __name__ == "__main__":
    app.debug = True
    app.run()



