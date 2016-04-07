from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base


def configure_db():
    db = SQLAlchemy()
    return db


def configure_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/fooflask'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


def bind_db_to_app(db, app):
    db.init_app(app)

Base = declarative_base()


class Personne(Base):
    __tablename__ = 'personne'
    name = Column(String, primary_key=True)


db = configure_db()
app = configure_app()
bind_db_to_app(db, app)


@app.route("/")
def hello():
    result = db.session.execute("select * from personne")
    return str(list(result))


@app.route("/add/<name>")
def add(name):
    personne = Personne(name=name)
    db.session.add(personne)
    db.session.commit()
    return ''


@app.before_first_request
def reset_db():
    db.session.execute("drop table if exists personne")
    db.session.execute("create table personne (name varchar)")
    db.session.execute("insert into personne (name) values ('moi')")
    db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)
