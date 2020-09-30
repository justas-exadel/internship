from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, \
    SubmitField, PasswordField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from flask_wtf.file import FileAllowed, FileField
from UtilitiesCalculator.models import User
from flask_login import current_user

class SignInForm(FlaskForm):
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember_psw = BooleanField("Remember me")
    submit = SubmitField('Submit')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('This email is not registered.')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirmed_psw = PasswordField('Repeat Password',
                                             validators=[DataRequired(),
                                                         EqualTo(
                                                             'password')])
    submit = SubmitField('Submit')


class SignUpForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    repeated_psw = PasswordField("Repeat password",  #doesn't validate
                                             [EqualTo('password',
                                                      "Passwords must match!")])
    submit = SubmitField('Submit')


    def validate(self):
        users = User.query.all()
        if users:
            raise ValidationError('User can be only one!')
        return True