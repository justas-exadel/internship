from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import Regexp


class Car_Form(FlaskForm):
    car_number = StringField('Car Number', [
        Regexp(regex=r'[A-Z]{3}[-]\d{3}', message='Car number format must be AAA-111')],
                         render_kw={'class': 'form-control'})
    submit = SubmitField('Submit', render_kw={'class': 'btn btn-success'})