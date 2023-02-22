# creating database models
# one for users, one for notes

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date=db.Column(db.DateTime(timezone=True), default = func.now())
    
    # associate notes to a user by setting up foreign key
    # one to many r/s: 1 user to many notes
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    # define all columns that want to be stored in this table
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name=db.Column(db.String(150))
    notes = db.relationship('Note') # everytime create a note, add to this user-note r/s