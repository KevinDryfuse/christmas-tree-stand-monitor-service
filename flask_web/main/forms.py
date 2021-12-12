from flask_wtf import FlaskForm
from sqlalchemy import func
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from flask_web import db
from flask_web.models import User


class Login(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class Register(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=64)], )
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=64)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password (at least 8 chars)', validators=[DataRequired(), Length(min=8), EqualTo('repeat_password',
                           message='Passwords must match')])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Register Account')

    # TODO: Tests
    def validate_email_not_already_registered(self):
        total_matches = db.session.query(User).filter(func.lower(User.email) == func.lower(self.email.data)).count()
        if total_matches > 0:
            return False
        else:
            return True


class EditProfile(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=64)])
    email = StringField('Email Address')
    submit = SubmitField('Update Profile')


class Add(FlaskForm):
    registration_id = StringField('Device Registration ID', validators=[DataRequired(), Length(min=1, max=10)])
    name = StringField('Device Name', validators=[DataRequired(), Length(min=1, max=64)])
    submit = SubmitField('Add Tree Stand')


class EditStand(FlaskForm):
    registration_id = StringField('Device Registration ID', validators=[DataRequired(), Length(min=1, max=10)])
    name = StringField('Device Name', validators=[DataRequired(), Length(min=1, max=64)])
    submit = SubmitField('Edit Tree Stand')

