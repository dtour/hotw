from application import app, db, bcrypt
from flask import flash, redirect, render_template, url_for, request
from application.forms import RegistrationForm, LoginForm, NewGroupForm
from application.models import User, Group, membership
from flask_login import login_user, current_user, logout_user, login_required

from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from datetime import datetime

# Routes
@app.route('/')
def index():#todo
    return render_template('index.html')

@app.route('/home')
@login_required
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
        # Hash password and store login info in db
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.email.data}!', category='success')
        return redirect(url_for('home'))


    return render_template('register.html', title='Register', form=form)

@app.route('/sign_in', methods=['GET','POST'])
def sign_in():#todo
    form = LoginForm()

    # Check if form was valid
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=True)

            # Redirect user to page that they were attempting to access before being prompted to login.
            # Use get method instead of trying to access dict through [] to avoid throwing error if arg does not exist
            next_page = request.args.get('next') 

            return redirect(next_page) if next_page else redirect(url_for('home'))

        else:
            flash('Login unsuccesful. Please check your email and password.')

    return render_template('sign_in.html', form=form)

@app.route('/sign_out')
@login_required
def sign_out():
    logout_user()
    return redirect('/')

@app.route('/account')
@login_required
def account():#todo
    return render_template('account.html')

@app.route('/change_password', methods=['GET','POST'])
@login_required
def change_password():#todo
    return "Hello World!"

@app.route('/new_group', methods=['GET','POST'])
@login_required
def new_group():#todo
    form = NewGroupForm()
    if form.validate_on_submit():
        flash('Your group has been created!', 'success')
        return redirect(url_for('home'))

    return render_template('new_group.html', form=form)