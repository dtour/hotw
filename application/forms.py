from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Email, EqualTo, ValidationError
from application.models import User

class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()

        if email:
            raise ValidationError('Email already in use')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class NewGroupForm(FlaskForm):
    group_name = StringField('Group name', validators=[InputRequired()])
    members_emails = TextAreaField("Members' emails (comma separated)")
    submit = SubmitField('Create group')