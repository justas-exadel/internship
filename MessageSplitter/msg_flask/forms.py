from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class Message_Form(FlaskForm):
    text = TextAreaField('Message Text', [DataRequired()],
                         render_kw={'class': 'form-control', 'rows': 10})
    max_length = IntegerField('Length', validators=[NumberRange(min=12, message='Message length have to be greater than 10')])
    submit = SubmitField('Submit', render_kw={'class': 'btn btn-success'})
