from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://comics:12345678@localhost:8889/comics'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)



class Comic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    issue_number = db.Column(db.Integer, nullable=False)
    year = db.Column(db.String(4), nullable=False)
    publisher_id = db.Column(db.Integer, ForeignKey("publisher.id"))

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

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Publisher {}>'.format(self.name)

@app.route("/")
def index():
    comics = Comic.query.all()
    return render_template('index.html', comics=comics)

if __name__ == "__main__":
    app.run()
