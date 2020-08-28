from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class Message_Form(FlaskForm):
    text = TextAreaField('Message Text', [DataRequired()],
                         render_kw={'class': 'form-control', 'rows': 10})
    max_length = IntegerField('Length', [DataRequired()])
    submit = SubmitField('Submit', render_kw={'class': 'btn btn-success'})
