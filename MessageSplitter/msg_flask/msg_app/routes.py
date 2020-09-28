from flask import render_template
from .forms import Message_Form
from .msg import Message_Splitter
from . import app

@app.route("/", methods=['GET'])
def home():
    return "<h1>Welcome to Message Splitter App</h1>"


@app.route("/split_message", methods=['GET', 'POST'])
def message_text():
    form = Message_Form()
    if form.validate_on_submit():
        text_data = form.text.data
        length_data = form.max_length.data
        splitted_msg = Message_Splitter(text_data, length_data).format()
        return render_template("msg_splitted.html", form=False,
                               data=splitted_msg)
    return render_template("index.html", form=form)



