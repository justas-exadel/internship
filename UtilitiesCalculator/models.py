from datetime import datetime

from flask import Blueprint, url_for
from quart import redirect
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import UtilitiesCalculator
from UtilitiesCalculator import db, app, ModelView, Admin, BaseView, expose


class User(db.Model, UserMixin):
    __tablename__ = "USER"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("Name", db.String(20), unique=True, nullable=False)
    email = db.Column("Email", db.String(120), unique=True,
                          nullable=False)
    password = db.Column("Password", db.String(60), unique=True,
                            nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class House(db.Model):
    __tablename__ = 'HOUSE'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column('Address', db.String, nullable=False)
    apartments_count = db.Column('Apartments Total', db.Integer, nullable=False)


class Apartment(db.Model):
    __tablename__ = 'APARTMENT'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column('Address', db.String, nullable=False)
    square_feet = db.Column('Square Feet (m3)', db.Float, nullable=True)


class Renter(db.Model):
    __tablename__ = 'RENTER'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Name', db.String, nullable=False)
    surname = db.Column('Surname', db.String, nullable=False)
    email = db.Column('Email', db.String, nullable=False)
    phone = db.Column('Phone', db.String, nullable=True)

class Service(db.Model):
    __tablename__ = 'SERVICE'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Name', db.String, nullable=False)


class ServiceCost(db.Model):
    __tablename__ = 'SERVICE_COST'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Name', db.String, nullable=False)
    cost = db.Column('Cost', db.Float, nullable=False)
    service_ID = db.Column(db.Integer, ForeignKey('SERVICE.id'))
    service = relationship("Service")

class Electricity(db.Model):
    __tablename__ = 'ELECTRICITY'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column('Year', db.Integer)
    month = db.Column('Month', db.Integer)
    apartment_ID = db.Column(db.Integer, ForeignKey('APARTMENT.id'))
    apartment = relationship("Apartment")
    consumption_from = db.Column('From', db.Integer)
    consumption_to = db.Column('To', db.Integer)
    difference = db.Column('Difference', db.Integer)
    cost_id = db.Column(db.Integer, ForeignKey('SERVICE_COST.id'))
    cost = relationship("ServiceCost")
    sum = db.Column('Sum', db.Float)


class Gas(db.Model):
    __tablename__ = 'GAS'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column('Year', db.Integer)
    month = db.Column('Month', db.Integer)
    apartment_ID = db.Column(db.Integer, ForeignKey('APARTMENT.id'))
    apartment = relationship("Apartment")
    consumption_from = db.Column('From', db.Integer)
    consumption_to = db.Column('To', db.Integer)
    difference = db.Column('Difference', db.Integer)
    cost_id = db.Column(db.Integer, ForeignKey('SERVICE_COST.id'))
    cost = relationship("ServiceCost")
    sum = db.Column('Sum', db.Float)


class HotWater(db.Model):
    __tablename__ = 'HOT_WATER'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column('Year', db.Integer)
    month = db.Column('Month', db.Integer)
    apartment_ID = db.Column(db.Integer, ForeignKey('APARTMENT.id'))
    apartment = relationship("Apartment")
    consumption_from = db.Column('From', db.Integer)
    consumption_to = db.Column('To', db.Integer)
    difference = db.Column('Difference', db.Integer)
    cost_id = db.Column(db.Integer, ForeignKey('SERVICE_COST.id'))
    cost = relationship("ServiceCost")
    sum = db.Column('Sum', db.Float)


class ColdWater(db.Model):
    __tablename__ = 'COLD_WATER'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column('Year', db.Integer)
    month = db.Column('Month', db.Integer)
    apartment_ID = db.Column(db.Integer, ForeignKey('APARTMENT.id'))
    apartment = relationship("Apartment")
    consumption_from = db.Column('From', db.Integer)
    consumption_to = db.Column('To', db.Integer)
    difference = db.Column('Difference', db.Integer)
    cost_id = db.Column(db.Integer, ForeignKey('SERVICE_COST.id'))
    cost = relationship("ServiceCost")
    sum = db.Column('Sum', db.Float)


class OtherUtilities(db.Model):
    __tablename__ = 'OTHER_UTILITIES'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column('Year', db.Integer)
    month = db.Column('Month', db.Integer)
    apartment_ID = db.Column(db.Integer, ForeignKey('APARTMENT.id'))
    apartment = relationship("Apartment")
    cost_id = db.Column(db.Integer, ForeignKey('SERVICE_COST.id'))
    cost = relationship("ServiceCost")
    sum = db.Column('Sum', db.Float)


class Rent(db.Model):
    __tablename__ = 'RENT'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column('Year', db.Integer)
    month = db.Column('Month', db.Integer)
    apartment_ID = db.Column(db.Integer, ForeignKey('APARTMENT.id'))
    apartment = relationship("Apartment")
    cost_id = db.Column(db.Integer, ForeignKey('SERVICE_COST.id'))
    cost = relationship("ServiceCost")
    sum = db.Column('Sum', db.Float)

class Report(db.Model):
    __tablename__ = 'REPORT'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    renter_ID = db.Column(db.Integer, ForeignKey('RENTER.id'))
    renter = relationship("Renter")
    electricity_ID = db.Column(db.Integer, ForeignKey('ELECTRICITY.id'))
    electricity = relationship("Electricity")
    gas_ID = db.Column(db.Integer, ForeignKey('GAS.id'))
    gas = relationship("Gas")
    hot_water_ID = db.Column(db.Integer, ForeignKey('HOT_WATER.id'))
    hot_water = relationship("HotWater")
    cold_water_ID = db.Column(db.Integer, ForeignKey('COLD_WATER.id'))
    cold_water = relationship("ColdWater")
    other_utilities_ID = db.Column(db.Integer, ForeignKey('OTHER_UTILITIES.id'))
    other_utilities = relationship("OtherUtilities")
    rent_ID = db.Column(db.Integer, ForeignKey('RENT.id'))
    rent = relationship("Rent")
    sum_total = db.Column('Total Eur', db.Float)


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.email == EMAIL_HOST_USER


admin = Admin(app, name='EDIT', template_mode='bootstrap3')
# admin = Blueprint('admin', __name__, url_prefix='/admin')
# current_app.config['INDEX_TEMPLATE']
# app.register_blueprint(admin)


class MyView(BaseView):
    @expose('/')
    def home(self):
        return redirect(url_for('home'))

admin.add_view(MyView(name='Utilities Calculator',endpoint='db'))
# from UtilitiesCalculator.models import User, House, Apartment, Renter, Service, ServiceCost, Electricity,Gas, ColdWater, HotWater, OtherUtilities, Rent, Report

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
admin.add_view(MyModelView(Report, db.session))
