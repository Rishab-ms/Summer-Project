from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:disha123@localhost/summer'
db = SQLAlchemy(app)


class Disha(db.Model):
    __tablename__='info'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))

db.create_all()
db.session.commit()

@app.route('/create',methods=['POST','GET'])
def create():
    if request.method == "GET":
		return render_template('/create.html')
    id=request.form['id']
    username = request.form['username']
    data = Disha(username=username, id=id)
    db.session.add(data)
    db.session.commit()
    return "Your data has been added"

if __name__ == "__main__":
    app.debug = True
    app.run()
