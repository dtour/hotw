from application import app
from flask import flash, redirect, render_template, url_for, request, session
from flask_session import Session
from application.forms import RegistrationForm, LoginForm
from application.models import User, Group, membership

from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

Session(app)

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

@app.route('/register', methods=['GET','POST'])
def register():#todo
    form = RegistrationForm()

    # Check if form was valid
    if form.validate_on_submit():
        flash(f'Account created for {form.email.data}!', category='success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/sign_in', methods=['GET','POST'])
def sign_in():#todo
    form = LoginForm()

    # Check if form was valid
    if form.validate_on_submit():
        if form.email.data == 'xx' and form.email.password == 'xx':
            return redirect(url_for('home'))

    return render_template('sign_in.html', form=form)

@app.route('/sign_out')
def sign_out():#todo
    return render_template('sign_out.html')

@app.route('/account')
def account():#todo
    return render_template('account.html')

@app.route('/change_password', methods=['GET','POST'])
def change_password():#todo
    return "Hello World!"