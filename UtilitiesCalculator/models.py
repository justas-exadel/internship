from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import LoginManager, current_user
from __init__ import db, app, admin
from flask_admin import BaseView, expose
from flask import redirect, url_for


class User(db.Model, UserMixin):
    __tablename__ = "USER"
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
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column('Address', db.String, nullable=False)
    apartments_count = db.Column('Apartments Total', db.Integer,
                                 nullable=False)


class Apartment(db.Model):
    __tablename__ = 'APARTMENT'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column('Address', db.String, nullable=False)
    square_feet = db.Column('Square Feet (m3)', db.Float, nullable=True)

    def __init__(self, address, square_feet):
        self.address = address
        self.square_feet = square_feet

    def __repr__(self):
        return self.address


class Renter(db.Model):
    __tablename__ = 'RENTER'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Name', db.String, nullable=False)
    surname = db.Column('Surname', db.String, nullable=False)
    email = db.Column('Email', db.String, nullable=False)
    phone = db.Column('Phone', db.String, nullable=True)


class Service(db.Model):
    __tablename__ = 'SERVICE'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Name', db.String, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class ServiceCost(db.Model):
    __tablename__ = 'SERVICE_COST'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Name', db.String, nullable=False)
    cost = db.Column('Cost', db.Float, nullable=False)
    service_ID = db.Column(db.Integer, ForeignKey('SERVICE.id'))
    service = relationship("Service")

    def __init__(self, name, cost, service_ID):
        self.name = name
        self.cost = cost
        self.service_ID = service_ID

    def __str__(self):
        return f" {self.name} - {self.cost} Eur"


class Electricity(db.Model):
    __tablename__ = 'ELECTRICITY'
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
    id = db.Column(db.Integer, primary_key=True)
    rent_ID = db.Column(db.Integer, ForeignKey('RENT.id'))
    rent = relationship("Rent")
    electricity_ID = db.Column(db.Integer, ForeignKey('ELECTRICITY.id'))
    electricity = relationship("Electricity")
    gas_ID = db.Column(db.Integer, ForeignKey('GAS.id'))
    gas = relationship("Gas")
    hot_water_ID = db.Column(db.Integer, ForeignKey('HOT_WATER.id'))
    hot_water = relationship("HotWater")
    cold_water_ID = db.Column(db.Integer, ForeignKey('COLD_WATER.id'))
    cold_water = relationship("ColdWater")
    other_utilities_ID = db.Column(db.Integer,
                                   ForeignKey('OTHER_UTILITIES.id'))
    other_utilities = relationship("OtherUtilities")
    sum_total = db.Column('Total Eur', db.Float)
    # status = db.Column('Status', db.String) #migrate


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
