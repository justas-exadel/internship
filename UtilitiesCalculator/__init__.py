from flask_admin import Admin
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from email_settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_USERNAME

basedir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

SECRET_KEY = os.urandom(33)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,
                                                                    'utilities.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()
db.metadata.clear()

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'Sign In'
login_manager.login_message_category = 'info'
login_manager.login_message = "Sign In is necessary"

mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = EMAIL_USERNAME
app.config['MAIL_PASSWORD'] = EMAIL_HOST_PASSWORD

admin = Admin(app, name='Utilities Calculator', template_mode='bootstrap3')

import routes
