from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Email, EqualTo, ValidationError, URL
from application.models import User

class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Email already in use')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign in')

class NewGroupForm(FlaskForm):
    group_name = StringField('Group name', validators=[InputRequired()])
    members_emails = TextAreaField("Members' emails (comma separated)")
    submit = SubmitField('Create group')

class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[InputRequired(), Email()])
    submit = SubmitField('Request password reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        
        if user is None:
            raise ValidationError('If an account with this email address exists, a password reset message will be sent shortly')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')

class SubmissionForm(FlaskForm):
    highlight = StringField('Your highlight', validators=[InputRequired(), URL()])
    submit = SubmitField('Submit highlight')