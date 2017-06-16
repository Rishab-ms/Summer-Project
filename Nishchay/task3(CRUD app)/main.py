from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
db = SQLAlchemy(app)

class Blog(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(30))
	author = db.Column(db.String(20))
	body = db.Column(db.Text)

	def __init__(self, title, author, body):
		self.title = title
		self.author = author
		self.body = body

db.create_all()
db.session.commit()

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/view_blog")
def view_blog():
	return render_template("view_blog.html", blogs = Blog.query.all())

@app.route("/create_blog", methods = ['GET', 'POST'])
def create_blog():
	if request.method == "POST":
		blog = Blog(request.form["title"], request.form["author"], request.form["body"])
		db.session.add(blog)
		db.session.commit()
		return redirect(url_for("view_blog"))
	return render_template("create_blog.html")

@app.route("/view_blog/delete_blog/<int:id>", methods = ['GET', 'DELETE'])
def delete_blog(id):
	db.session.delete(Blog.query.get(id))
	db.session.commit()
	return redirect(url_for("view_blog"))

@app.route("/view_blog/edit_blog/<int:id>", methods = ['GET', 'POST'])
def edit_blog(id):
	blog = db.session.query(Blog).filter(Blog.id==id).first()
	if request.method == "POST":
		blog.title = request.form["title"]
		blog.author = request.form["author"]
		blog.body = request.form["body"]
		db.session.commit()
		return redirect(url_for("view_blog"))
	return render_template("edit_blog.html")

if __name__ == " __main__":
	app.run(debug=True)