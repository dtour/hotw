import os

from flask import Flask, flash, redirect, render_template, url_for, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# SQL Alchemcy config
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#         'sqlite:///' + os.path.join(basedir, 'app.db')
# SQLALCHEMY_TRACK_MODIFICATIONS = False

# Routes
@app.route('/')
def index():#todo
    return render_template('index.html')

# @login_required
@app.route('/home')
def home():#todo
    return render_template('home.html')

@app.route('/about')
def about():#todo
    return render_template('about.html')
    
@app.route('/help')
def help():#todo
    return render_template('help.html')

@app.route('/contact')
def contact():#todo
    return render_template('contact.html')

@app.route('/sign_in')
def sign_in():#todo
    return render_template('sign_in.html')

@app.route('/sign_out')
def sign_out():#todo
    return render_template('sign_out.html')

@app.route('/account')
def account():#todo
    return render_template('account.html')

@app.route('/change_password')
def change_password():#todo
    return "Hello World!"
