from application import app, db, bcrypt, mail
from flask import flash, redirect, render_template, url_for, request
from application.forms import (RegistrationForm, LoginForm, NewGroupForm, 
                               RequestResetForm, ResetPasswordForm)
from application.models import User, Group, membership
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

# Routes
@app.route('/')
def index():#todo
    return render_template('index.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    # Check if form was valid
    if form.validate_on_submit():
        # Hash password and store login info in db
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        flash(f'Account created for {form.email.data}!', category='success')
        return redirect(url_for('home'))

    
    return render_template('register.html', title='Register', form=form)

@app.route('/sign_in', methods=['GET','POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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

@app.route('/group/new', methods=['GET','POST'])
@login_required
def new_group():#todo
    form = NewGroupForm()
    if form.validate_on_submit():
        # Add new group to database
        group = Group(name=form.group_name.data, creator_id=current_user.get_id())
        db.session.add(group)
        db.session.commit()
        # Process members_email field into seperate emails
        members_emails = ''.join(form.members_emails.data.split()).split(sep=',')
        # Send emails to potential members asking if they want to join

        #do the below 3 steps in a new function
        # If they confirm they want to join, add User to memberships table

        # If they join, ask them to create an account if they don't have one

        # After they create an account, automatically add user to memberships table
        



        flash('Your group has been created! Members have been emailed a confirmation link.', 'success')
        return redirect(url_for('home'))

    return render_template('new_group.html', form=form)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='dtour@hotw.app', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link within the next hour:
{url_for('reset_token', token=token, _external=True)}
    
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_request.html', form=form)

@app.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)

    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Hash password and store login info in db
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password_hash = hashed_password
        db.session.commit()
        login_user(user, remember=True)
        flash(f'Your password has been updated', category='success')
        return redirect(url_for('home'))

    return render_template('reset_token.html', form=form) 
