from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, \
     check_password_hash
import os

app = Flask(__name__)
app.secret_key = "9999"

app.config["TESTING"] = False
app.config["LOGIN_DISABLED"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	username = db.Column(db.String(20))
	password = db.Column(db.String(20))

	def __init__(self, username, password):
		self.username = username
		self.password = generate_password_hash(password)

	def is_active(self):
		return True

	def get_id(self):
		return self.id

	def is_authenticated(self):
		return self.authenticated

	def is_anonymous(self):
		return False

db.create_all()
db.session.commit()

@login_manager.user_loader
def user_loader(id):
	return User.query.get(id)

@app.route("/register/", methods = ["POST"])
def register():
	user = User(request.json.get("username", ""), request.json.get("password", ""))
	if db.session.query(User.username).filter(User.username == user.username).count() > 0:
		response = {"message": "username not unique"}
		return jsonify(response)
	else:
		db.session.add(user)
		db.session.commit()
		response = {"message": "new user registered"}
		return jsonify(response)

@app.route("/login/", methods = ["POST"])
def login():
	candidate_username = request.json.get("username", "")
	candidate_password = request.json.get("password", "")
	if db.session.query(User.username).filter(User.username == candidate_username).count() > 0:
		user = db.session.query(User).filter(User.username == candidate_username).first()
		if check_password_hash(user.password, candidate_password):
			login_user(user, remember=True)
			response = {"message": "user logged in"}
			return jsonify(response)
		else:
			response = {"message": "incorrect password"}
			return jsonify(response)
	else:
		response = {"message": "invalid username"}
		return jsonify(response)

@app.route("/secret/")
@login_required
def secret():
	response = {"message": "secret stuff"}
	return jsonify(response)

@app.route("/logout/")
@login_required
def logout():
	logout_user()
	response = {"message": "user logged out"}
	return jsonify(response)
	

if __name__ == "__main__":
	app.run(debug = True)