from sqlalchemy.orm import relationship
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from __init__ import db, app


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

    def __init__(self, address, apartments_count):
        self.address = address
        self.apartments_count = apartments_count

    def __repr__(self):
        return self.address


class ApartmentStatus(db.Model):
    __tablename__ = 'APARTMENT_STATUS'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, nullable=False)

    def __init__(self, status):
        self.status = status

    def __repr__(self):
        return self.status


class Apartment(db.Model):
    __tablename__ = 'APARTMENT'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column('Address', db.String, nullable=False)
    square_feet = db.Column('Square Feet (m3)', db.Float, nullable=True)
    house_ID = db.Column(db.Integer, ForeignKey('HOUSE.id'))
    house = relationship("House")
    status_ID = db.Column(db.Integer, ForeignKey(
        'APARTMENT_STATUS.id'))
    status = relationship("ApartmentStatus")

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
    apartment_ID = db.Column(db.Integer, ForeignKey('APARTMENT.id'))
    apartment = relationship("Apartment")


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


class Utility(db.Model):
    __abstract__ = True
    year = db.Column('Year', db.Integer, nullable=False)
    month = db.Column('Month', db.Integer, nullable=False)
    sum = db.Column('Sum', db.Float)


class Consumption(db.Model):
    __abstract__ = True
    consumption_from = db.Column('From', db.Integer)
    consumption_to = db.Column('To', db.Integer)
    difference = db.Column('Difference', db.Integer)


class Electricity(Utility, Consumption):
    __tablename__ = 'ELECTRICITY'
    id = db.Column(db.Integer, primary_key=True)
    apartment_ID = db.Column(db.Integer, ForeignKey('APARTMENT.id'))
    apartment = relationship("Apartment")
    cost_ID = db.Column(db.Integer, ForeignKey('SERVICE_COST.id'))
    cost = relationship("ServiceCost")

    def __repr__(self):
        return f'{self.apartment}'


class Gas(Utility, Consumption):
    __tablename__ = 'GAS'
    id = db.Column(db.Integer, primary_key=True)
    apartment_ID = db.Column(db.Integer, ForeignKey('APARTMENT.id'))
    apartment = relationship("Apartment")
    cost_ID = db.Column(db.Integer, ForeignKey('SERVICE_COST.id'))
    cost = relationship("ServiceCost")


class HotWater(Utility, Consumption):
    __tablename__ = 'HOT_WATER'
    id = db.Column(db.Integer, primary_key=True)
    apartment_ID = db.Column(db.Integer, ForeignKey('APARTMENT.id'))
    apartment = relationship("Apartment")
    cost_ID = db.Column(db.Integer, ForeignKey('SERVICE_COST.id'))
    cost = relationship("ServiceCost")


class ColdWater(Utility, Consumption):
    __tablename__ = 'COLD_WATER'
    id = db.Column(db.Integer, primary_key=True)
    apartment_ID = db.Column(db.Integer, ForeignKey('APARTMENT.id'))
    apartment = relationship("Apartment")
    cost_ID = db.Column(db.Integer, ForeignKey('SERVICE_COST.id'))
    cost = relationship("ServiceCost")


class OtherUtilities(Utility):
    __tablename__ = 'OTHER_UTILITIES'
    id = db.Column(db.Integer, primary_key=True)
    apartment_ID = db.Column(db.Integer, ForeignKey('APARTMENT.id'))
    apartment = relationship("Apartment")
    cost_ID = db.Column(db.Integer, ForeignKey('SERVICE_COST.id'))
    cost = relationship("ServiceCost")


class Rent(Utility):
    __tablename__ = 'RENT'
    id = db.Column(db.Integer, primary_key=True)
    apartment_ID = db.Column(db.Integer, ForeignKey('APARTMENT.id'))
    apartment = relationship("Apartment")
    cost_ID = db.Column(db.Integer, ForeignKey('SERVICE_COST.id'))
    cost = relationship("ServiceCost")


class Report(db.Model):
    __tablename__ = 'REPORT'
    id = db.Column(db.Integer, primary_key=True)
    rent_ID = db.Column(db.Integer, ForeignKey('RENT.id'))
    rent = relationship("Rent", single_parent=True,
                        cascade="all, delete-orphan")
    electricity_ID = db.Column(db.Integer, ForeignKey('ELECTRICITY.id'))
    electricity = relationship("Electricity", single_parent=True,
                               cascade="all, delete-orphan")
    gas_ID = db.Column(db.Integer, ForeignKey('GAS.id'))
    gas = relationship("Gas", single_parent=True, cascade="all, delete-orphan")
    hot_water_ID = db.Column(db.Integer, ForeignKey('HOT_WATER.id'))
    hot_water = relationship("HotWater", single_parent=True,
                             cascade="all, delete-orphan")
    cold_water_ID = db.Column(db.Integer, ForeignKey('COLD_WATER.id'))
    cold_water = relationship("ColdWater", single_parent=True,
                              cascade="all, delete-orphan")
    other_utilities_ID = db.Column(db.Integer,
                                   ForeignKey('OTHER_UTILITIES.id'))
    other_utilities = relationship("OtherUtilities", single_parent=True,
                                   cascade="all, delete-orphan")
    sum_total = db.Column('Total Eur', db.Float)
    sent_ID = db.Column(db.Integer, ForeignKey('REPORT_STATUS.id'))
    sent = relationship("ReportStatus")


class ReportStatus(db.Model):
    __tablename__ = 'REPORT_STATUS'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, nullable=False)

    def __init__(self, status):
        self.status = status

    def __repr__(self):
        return self.status
