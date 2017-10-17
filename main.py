from flask import Flask, request, redirect, render_template, make_response
from app import app
from models import Comic, Publisher
import cgi
from datetime import datetime


@app.route("/")
def index():
    #check what the last visited comic was
    comic = None
    last_viewed_comic_id = request.cookies.get('last-viewed-comic-id')
    if last_viewed_comic_id:
        comic = Comic.query.get(last_viewed_comic_id)
        print('last viewed comic id', last_viewed_comic_id)

    # Check for referrer query param
    referrer = request.args.get('referrer')
    if referrer:
        print('referred by', referrer)

    # return all comics or filter by publisher_id
    publisher_id = request.args.get('publisher_id')
    publisher = None
    if publisher_id:
        #comics = Comic.query.filter_by(publisher_id=publisher_id)
        publisher = Publisher.query.get(publisher_id)
        comics = publisher.comics
    else:
        comics = Comic.query.all()

    # set a last visited cookie
    response = make_response(render_template('index.html', comics=comics, last_viewed_comic=comic, publisher=publisher))
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
