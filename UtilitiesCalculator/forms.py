from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, \
    SubmitField, PasswordField, FloatField, SelectField
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

    def validate_user(self, email):
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

class UtilitiesForm(FlaskForm):
    electricity_to = IntegerField('To', validators=[DataRequired()])
    electricity_from = IntegerField('From', validators=[DataRequired()])
    electricity_cost = FloatField('Cost', validators=[DataRequired()])
    gas_to = IntegerField('To', validators=[DataRequired()])
    gas_from = IntegerField('From', validators=[DataRequired()])
    gas_cost = FloatField('Cost', validators=[DataRequired()])
    cold_water_to = IntegerField('To')
    cold_water_from = IntegerField('From')
    cold_water_cost = FloatField('Cost')
    hot_water_to = IntegerField('To')
    hot_water_from = IntegerField('From')
    hot_water_cost = FloatField('Cost')
    other_ut_cost = FloatField('Cost')
    rent_cost = FloatField('Cost')
    year = SelectField('Year', choices=[('2020', 2020), ('2021', 2021)])
    month = SelectField('Month', choices=[('1', 1), ('2', 2)])
    apartment = SelectField('Apartment', choices=[('Apartment1', 'apartment1'), ('Apartment2', 'apartment2')])
    submit = SubmitField('Calculate')
    confirm = SubmitField('Confirm')



