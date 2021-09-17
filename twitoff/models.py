

from flask_sqlalchemy import SQLAlchemy

# update models.py
# don't use this line -- from .models import db, User
import os

app_dir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///{}".format(os.path.join(app_dir, "twitoff.sqlite3"))


db = SQLAlchemy()

# Creates a 'user' table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # id as primary key
    name = db.Column(db.String(50), nullable=False) # user name

    def __repr__(self):
        return "<User: {}>".format(self.name)

# Creates a 'Tweet' table
class Tweet(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    text = db.Column(db.Unicode(300), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tweets', lazy=True))
    embedding = db.Column(db.PickleType, nullable=False)


    def __repr__(self):
        return f'[Tweet: {self.text}]'