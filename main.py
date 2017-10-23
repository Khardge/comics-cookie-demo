from flask import Flask, request, redirect, render_template, make_response, flash, session
from app import app
from models import Comic, Publisher, User, db
import cgi
from datetime import datetime

#-------------------------
# Route handlers
#-------------------------
@app.before_request
def require_login():
    if not ('email' in session or request.endpoint in ['login', 'register']):
        return redirect("/login")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    #User must be POSTing form, so validate email and password
    email = request.form['email']
    password = request.form['password']
    users = User.query.filter_by(email=email)
    if users.count() == 1:
        #email and password were correct
        #put user.email into session to keep user logged in
        user = users.first()
        if password == user.password:
            log_user_in(user)
            flash('welcome back, '+user.email)
            return redirect("/")

    #if we got here, then the email or password was incorrect
    flash('bad username or password')
    return redirect("/login")

@app.route("/logout", methods=['POST'])
def logout():
    #delete the email stored in the session
    log_user_out()
    return redirect("/")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        if not is_email(email):
            flash('zoiks! "' + email + '" does not seem like an email address')
            return redirect('/register')
        email_db_count = User.query.filter_by(email=email).count()
        if email_db_count > 0:
            flash('yikes! "' + email + '" is already taken and password reminders are not implemented')
            return redirect('/register')
        if password != verify:
            flash('passwords did not match')
            return redirect('/register')
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        log_user_in(user)
        return redirect("/")
    else:
        return render_template('register.html')

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


#-------------------------
# Util functions
#-------------------------
def logged_in_user():
    owner = User.query.filter_by(email=session['email']).first()
    return owner

def is_email(string):
    # for our purposes, an email string has an '@' followed by a '.'
    # there is an embedded language called 'regular expression' that would crunch this implementation down
    # to a one-liner, but we'll keep it simple:
    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    if not atsign_present:
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present

def log_user_out():
    del session['email']

def log_user_in(user):
    ### Logic for logging in a user
    session['email'] = user.email

if __name__ == "__main__":
    app.run()
