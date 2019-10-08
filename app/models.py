from app import db

# Tells us how to create a schema

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # Tells Python how to print object of this class
    def __repr__(self):
        return '<User {}>'.format(self.username) 
        