from datetime import datetime
from app import db

# Tells us how to create a schema

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # Tells Python how to print object of this class
    def __repr__(self):
        return '<User {}>'.format(self.username) 

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140), index=True)
    # Passing function as default value results in setting the field to the value of calling such function (not the result of calling it)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # feeds id value from 'user' table

    
    def __repr__(self):
        return '<Post {}>'.format(self.body) 