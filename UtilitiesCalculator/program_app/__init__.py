from flask_admin import Admin
from flask_mail import Mail
from flask_bcrypt import Bcrypt
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_USERNAME, \
    SECRET_KEY
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask import redirect, url_for
from flask_login import LoginManager, current_user

# from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,
                                                                    'utilities.sqlite')
app.config['USE_SESSION_FOR_NEXT'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.metadata.clear()

# Migrate(app, db)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'sign_in'
login_manager.login_message_category = 'info'
login_manager.login_message = "You need to sign up!"

mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = EMAIL_USERNAME
app.config['MAIL_PASSWORD'] = EMAIL_HOST_PASSWORD

admin = Admin(app, name='Utilities Calculator', template_mode='bootstrap3')

import program_app.views
from .models import Service, ApartmentStatus, ReportStatus, User, House, \
    Apartment, Renter, ServiceCost, Electricity, Gas, ServiceCost, HotWater, \
    ColdWater, OtherUtilities, Rent

if 'utilities.sqlite' not in os.listdir():
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.add(ApartmentStatus(status='RENT'))
        db.session.add(ApartmentStatus(status='MAIN'))
        db.session.add(ReportStatus(status='YES'))
        db.session.add(ReportStatus(status='NO'))
        db.session.add(Service('Electricity'))
        db.session.add(Service('Gas'))
        db.session.add(Service('Hot Water'))
        db.session.add(Service('Cold Water'))
        db.session.add(Service('Rent'))
        db.session.add(Service('Other Utilities'))
        db.session.commit()


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.email == "viskoniekas@gmail.com"


class MyView(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('home'))


admin.add_view(MyView(name='Back to Page'))
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(House, db.session))
admin.add_view(MyModelView(Apartment, db.session))
admin.add_view(MyModelView(Renter, db.session))
admin.add_view(MyModelView(Service, db.session))
admin.add_view(MyModelView(ServiceCost, db.session))
admin.add_view(MyModelView(Electricity, db.session))
admin.add_view(MyModelView(Gas, db.session))
admin.add_view(MyModelView(HotWater, db.session))
admin.add_view(MyModelView(ColdWater, db.session))
admin.add_view(MyModelView(OtherUtilities, db.session))
admin.add_view(MyModelView(Rent, db.session))
