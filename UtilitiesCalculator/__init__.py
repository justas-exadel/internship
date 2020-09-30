from flask_admin import Admin, BaseView, expose
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from email_settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_USERNAME
from flask_admin.contrib.sqla import ModelView


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
SECRET_KEY = os.urandom(33)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,
                                                                    'utilities.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()

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

import UtilitiesCalculator.routes


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.email == EMAIL_HOST_USER


admin = Admin(app, name='EDIT', template_mode='bootstrap3')


class MyView(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('index'))


admin.add_view(MyView(name='Utilities Calculator'))

# admin.add_view(MyModelView(PajamuIrasas, db.session))
# admin.add_view(MyModelView(IslaiduIrasas, db.session))
# admin.add_view(MyModelView(Vartotojas, db.session))
# from UtilitiesCalculator.models import User


