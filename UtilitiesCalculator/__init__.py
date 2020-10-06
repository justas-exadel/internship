from flask_admin import Admin
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from email_settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_USERNAME
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask import redirect, url_for
from flask_login import LoginManager, current_user

basedir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

SECRET_KEY = os.urandom(33)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,
                                                                    'utilities.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
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

import views
from models import *

if 'utilities.sqlite' not in os.listdir():
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.add(Service('Electricity'))
        db.session.add(Service('Gas'))
        db.session.add(Service('Hot Water'))
        db.session.add(Service('Cold Water'))
        db.session.add(Service('Rent'))
        db.session.add(Service('Other Utilities'))
        db.session.add(ApartmentStatus(status='RENT'))
        db.session.add(ApartmentStatus(status='MAIN'))
        db.session.add(ReportStatus(status='YES'))
        db.session.add(ReportStatus(status='NO'))
        db.session.commit()


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class MyView(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('home'))


admin.add_view(MyView(name='Back to Page'))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(House, db.session))
admin.add_view(ModelView(Apartment, db.session))
admin.add_view(ModelView(Renter, db.session))
admin.add_view(ModelView(Service, db.session))
admin.add_view(ModelView(ServiceCost, db.session))
admin.add_view(ModelView(Electricity, db.session))
admin.add_view(ModelView(Gas, db.session))
admin.add_view(ModelView(HotWater, db.session))
admin.add_view(ModelView(ColdWater, db.session))
admin.add_view(ModelView(OtherUtilities, db.session))
admin.add_view(ModelView(Rent, db.session))
admin.add_view(ModelView(Report, db.session))
