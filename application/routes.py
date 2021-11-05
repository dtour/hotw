import datetime
from application import app, db, bcrypt
from flask import flash, redirect, render_template, url_for, request
from application.forms import (RegistrationForm, LoginForm, NewGroupForm, 
                               RequestResetForm, ResetPasswordForm, SubmissionForm)
from application.models import Submission, User, Group
from application.email_helpers import send_reset_email, send_join_group_email, send_all_highlight_email
from flask_login import login_user, current_user, logout_user, login_required
from apscheduler.schedulers.background import BackgroundScheduler

# Background scheduler to send weekly emails
sched = BackgroundScheduler(daemon=True)
sched.add_job(send_all_highlight_email,'cron',day_of_week='sun',hour='8',timezone='utc')
sched.start()

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/home', methods=['GET','POST'])
@login_required
def home():
    my_groups = []
    i=0
    for group in current_user.membership:
        if Submission.query.filter_by(user_id=current_user.get_id(), group_id=group.id,
                                      week=datetime.datetime.utcnow().isocalendar().week).first():
            submission_status = True
        else:
            submission_status = False

        # Generate unique instance of form
        i =+ 1
        form = SubmissionForm(prefix=i)
        my_groups.append([group, submission_status, form])

        if form.validate_on_submit():
            submission = Submission(user_id=current_user.get_id(), group_id=group.id,
                                      week=datetime.datetime.utcnow().isocalendar().week, submission_text=form.highlight.data)
            db.session.add(submission)
            db.session.commit()
            flash(f'Your highlight has been submitted!', category='success')
            return redirect(url_for('home'))

    return render_template('home.html', my_groups=my_groups)

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

@app.route('/new_group', methods=['GET','POST'])
@login_required
def new_group():#todo
    form = NewGroupForm()
    if form.validate_on_submit():
        # Add new group to database and add creator to memberships table
        group = Group(name=form.group_name.data, creator_id=current_user.get_id())
        db.session.add(group)
        group.members.append(current_user)
        db.session.commit()
        # Process members_email field into seperate emails
        members_emails = ''.join(form.members_emails.data.split()).split(sep=',')
        # Send emails to potential members asking if they want to join
        for invitee in members_emails:
            send_join_group_email(group, current_user, invitee)
            # drop existing group first to avoid overlap
        flash('Your group has been created! Members have been emailed an invitation.', 'success')
        return redirect(url_for('home'))

    return render_template('new_group.html', form=form)

@app.route('/join_group/<token>')
@login_required
def join_group(token):
    group = Group.verify_join_group_token(token)

    if not group:
        flash('That is an invalid or expired invitation', 'danger')
        return redirect(url_for('home'))
    
    group.members.append(current_user)
    db.session.commit()
    flash(f'You have joined {group.name}!', category='success')
    return redirect(url_for('home'))

@app.route('/reset_password', methods=['GET','POST'])
def reset_request():
    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', category='success')
        return redirect(url_for('sign_in'))
    return render_template('reset_request.html', form=form)

@app.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    user = User.verify_reset_token(token)

    if not user:
        flash('That is an invalid or expired token', 'danger')
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
