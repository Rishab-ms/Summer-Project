from flask import Flask, jsonify, request
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

	def serialize(self):
		return {
		'id' : self.id,
		'title' : self.title,
		'author' : self.author,
		'body' : self.body
		}


db.create_all()
db.session.commit()

@app.route("/read/")
def read():
	blogs = Blog.query.all()
	json_ready = [blog.serialize() for blog in blogs]
	return jsonify(json_ready)

@app.route("/read/<int:id>/")
def readById(id):
	blog = Blog.query.get(id)
	json_ready = [blog.serialize()]
	return jsonify(json_ready)

@app.route("/create/", methods=["POST"])
def create():
	blog = Blog(request.json.get('title', ''), request.json.get('author', ''),request.json.get('body', ''))
	db.session.add(blog)
	db.session.commit()
	return "created"

@app.route("/delete/<int:id>/", methods=["DELETE"])
def delete(id):
	blog = Blog.query.get(id)
	db.session.delete(blog)
	db.session.commit()
	return "deleted"

@app.route("/update/<int:id>/", methods=["PUT"])
def update(id):
	blog = Blog.query.get(id)
	blog.title = request.json.get('title', blog.title)
	blog.author = request.json.get('author', blog.author)
	blog.body = request.json.get('body', blog.body)
	db.session.commit()
	return "updated"

if __name__ == "__main__":
	app.run(debug = True)