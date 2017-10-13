from flask import Flask, request, redirect, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
import cgi
from datetime import datetime

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
    #check what the last visited comic was
    last_viewed_comic_id = request.cookies.get('last-viewed-comic-id')
    if last_viewed_comic_id:
        comic = Comic.query.get(last_viewed_comic_id)
        print('last viewed comic id', last_viewed_comic_id)

    # Check for referrer query param
    referrer = request.args.get('referrer')
    if referrer:
        print('referred by', referrer)

    # set a last visited cookie
    comics = Comic.query.all()
    response = make_response(render_template('index.html', comics=comics, last_viewed_comic=comic))
    response.set_cookie('last-visited-index', datetime.now().strftime('%m/%d/%Y'), max_age=60*60*24*365)

    return response

@app.route('/comic/<comic_id>')
def comic(comic_id):
    #get comic from db
    comic = Comic.query.get(comic_id)

    #set last viewed comic id in a cookie
    response = make_response(render_template('comic.html', comic=comic))
    response.set_cookie('last-viewed-comic-id', str(comic.id), max_age=60*60*24*365)
    return response

if __name__ == "__main__":
    app.run()
