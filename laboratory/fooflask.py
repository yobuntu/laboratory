from flask import Flask
import threading
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/fooflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#db.session.execute("drop table if exists personne")
#db.session.execute("create table personne (name varchar)")
#db.session.execute("insert into personne (name) values ('moi')")
#db.session.commit()

class Personne(db.Model):
    __tablename__ = 'personne'
    name = Column(String, primary_key=True)


@app.route("/")
def hello():
    result = db.session.execute("select * from personne")
    return str(list(result))


@app.route("/add/<name>")
def add(name):
    for i in range(10):
        personne = Personne(name="{}{}".format(name, i))
        db.session.add(personne)
        db.session.commit()
    return ''


@app.route("/test")
def test():
    p = Personne(name='toto')
    db.session.add(p)
    db.session.query(Personne).all()
    return ''

if __name__ == "__main__":
    app.run(debug=True)
