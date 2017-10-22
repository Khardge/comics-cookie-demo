from sqlalchemy import ForeignKey
from app import db

class Comic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    issue_number = db.Column(db.Integer, nullable=False)
    year = db.Column(db.String(4), nullable=False)
    publisher_id = db.Column(db.Integer, ForeignKey("publisher.id"))
    publisher = db.relationship('Publisher')

    def __init__(self, title, issue_number, year, publisher_id):
        self.title = title
        self.year = year
        self.issue_number = issue_number
        self.publisher_id = publisher_id

    def __repr__(self):
        return '<Comic {title}, {year}>'.format(title=self.title, year=self.year)

class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    comics = db.relationship('Comic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Publisher {name}>'.format(name=self.name)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User {email}>'.format(email=self.email)
