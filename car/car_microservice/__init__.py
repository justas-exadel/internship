from flask import Flask
from flask_json import FlaskJSON
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
FlaskJSON(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,
                                                                    'cars.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
