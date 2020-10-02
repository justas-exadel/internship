from flask_admin import Admin, BaseView, expose
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
import os
from flask import Flask, redirect, url_for, current_app
from flask_sqlalchemy import SQLAlchemy
from UtilitiesCalculator.email_settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_USERNAME
from flask_admin.contrib.sqla import ModelView



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


# class MyModelView(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated and \
#                current_user.email == EMAIL_HOST_USER
#
#
# admin = Admin(app, name='EDIT', template_mode='bootstrap3')
#
# class MyView(BaseView):
#     @expose('/')
#     def home(self):
#         return redirect(url_for('home'))
#
# admin.add_view(MyView(name='Utilities Calculator'))
# from UtilitiesCalculator.models import User, House, Apartment, Renter, Service, ServiceCost, Electricity,Gas, ColdWater, HotWater, OtherUtilities, Rent, Report
#
# admin.add_view(MyModelView(User, db.session))
# admin.add_view(MyModelView(House, db.session))
# admin.add_view(MyModelView(Apartment, db.session))
# admin.add_view(MyModelView(Renter, db.session))
# admin.add_view(MyModelView(Service, db.session))
# admin.add_view(MyModelView(ServiceCost, db.session))
# admin.add_view(MyModelView(Electricity, db.session))
# admin.add_view(MyModelView(Gas, db.session))
# admin.add_view(MyModelView(HotWater, db.session))
# admin.add_view(MyModelView(ColdWater, db.session))
# admin.add_view(MyModelView(OtherUtilities, db.session))
# admin.add_view(MyModelView(Rent, db.session))
# admin.add_view(MyModelView(Report, db.session))







