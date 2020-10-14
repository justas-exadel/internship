from sqlalchemy.orm import relationship
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db, app


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
    address = db.Column('Address', db.String(100), nullable=False)
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
    status = db.Column(db.String(100), nullable=False)

    def __init__(self, status):
        self.status = status

    def __repr__(self):
        return self.status


class Apartment(db.Model):
    __tablename__ = 'APARTMENT'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column('Address', db.String(100), nullable=False)
    square_feet = db.Column('Square Feet (m3)', db.Float, nullable=True)
    house_ID = db.Column(db.Integer, db.ForeignKey('HOUSE.id'))
    house = db.relationship("House")
    status_ID = db.Column(db.Integer, db.ForeignKey(
        'APARTMENT_STATUS.id'))
    status = db.relationship("ApartmentStatus")
    renter = db.relationship("Renter")

    def __init__(self, address, square_feet):
        self.address = address
        self.square_feet = square_feet

    def get_renter_email(self):
        renter = Renter.query.filter_by(id=self.id).first()
        return renter.email

    def __repr__(self):
        return self.address


class Renter(db.Model):
    __tablename__ = 'RENTER'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Name', db.String(100), nullable=False)
    surname = db.Column('Surname', db.String(100), nullable=False)
    email = db.Column('Email', db.String(100), nullable=False)
    phone = db.Column('Phone', db.String(100), nullable=True)
    apartment_ID = db.Column(db.Integer, db.ForeignKey(
        'APARTMENT.id'))
    apartment = db.relationship('Apartment')

    def __init__(self, name, surname, email, phone):
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone

    def __repr__(self):
        return f'{self.name} {self.surname}'


class Service(db.Model):
    __tablename__ = 'SERVICE'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Name', db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class ServiceCost(db.Model):
    __tablename__ = 'SERVICE_COST'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Name', db.String(100), nullable=False)
    cost = db.Column('Cost', db.Float, nullable=False)
    service_ID = db.Column(db.Integer, db.ForeignKey('SERVICE.id'))
    service = db.relationship("Service")

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
    apartment_ID = db.Column(db.Integer, db.ForeignKey('APARTMENT.id'))
    apartment = db.relationship("Apartment")
    cost_ID = db.Column(db.Integer, db.ForeignKey('SERVICE_COST.id'))
    cost = db.relationship("ServiceCost")

    def __repr__(self):
        return f'{self.apartment}'


class Gas(Utility, Consumption):
    __tablename__ = 'GAS'
    id = db.Column(db.Integer, primary_key=True)
    apartment_ID = db.Column(db.Integer, db.ForeignKey('APARTMENT.id'))
    apartment = db.relationship("Apartment")
    cost_ID = db.Column(db.Integer, db.ForeignKey('SERVICE_COST.id'))
    cost = db.relationship("ServiceCost")


class HotWater(Utility, Consumption):
    __tablename__ = 'HOT_WATER'
    id = db.Column(db.Integer, primary_key=True)
    apartment_ID = db.Column(db.Integer, db.ForeignKey('APARTMENT.id'))
    apartment = db.relationship("Apartment")
    cost_ID = db.Column(db.Integer, db.ForeignKey('SERVICE_COST.id'))
    cost = db.relationship("ServiceCost")


class ColdWater(Utility, Consumption):
    __tablename__ = 'COLD_WATER'
    id = db.Column(db.Integer, primary_key=True)
    apartment_ID = db.Column(db.Integer, db.ForeignKey('APARTMENT.id'))
    apartment = db.relationship("Apartment")
    cost_ID = db.Column(db.Integer, db.ForeignKey('SERVICE_COST.id'))
    cost = db.relationship("ServiceCost")


class OtherUtilities(Utility):
    __tablename__ = 'OTHER_UTILITIES'
    id = db.Column(db.Integer, primary_key=True)
    apartment_ID = db.Column(db.Integer, db.ForeignKey('APARTMENT.id'))
    apartment = db.relationship("Apartment")
    cost_ID = db.Column(db.Integer, db.ForeignKey('SERVICE_COST.id'))
    cost = db.relationship("ServiceCost")


class Rent(Utility):
    __tablename__ = 'RENT'
    id = db.Column(db.Integer, primary_key=True)
    apartment_ID = db.Column(db.Integer, db.ForeignKey('APARTMENT.id'))
    apartment = db.relationship("Apartment")
    cost_ID = db.Column(db.Integer, db.ForeignKey('SERVICE_COST.id'))
    cost = db.relationship("ServiceCost")


class Report(db.Model):
    __tablename__ = 'REPORT'
    id = db.Column(db.Integer, primary_key=True)
    rent_ID = db.Column(db.Integer, db.ForeignKey('RENT.id'))
    rent = db.relationship("Rent", single_parent=True,
                        cascade="all, delete-orphan")
    electricity_ID = db.Column(db.Integer, db.ForeignKey('ELECTRICITY.id'))
    electricity = db.relationship("Electricity", single_parent=True,
                               cascade="all, delete-orphan")
    gas_ID = db.Column(db.Integer, db.ForeignKey('GAS.id'))
    gas = db.relationship("Gas", single_parent=True, cascade="all, delete-orphan")
    hot_water_ID = db.Column(db.Integer, db.ForeignKey('HOT_WATER.id'))
    hot_water = db.relationship("HotWater", single_parent=True,
                             cascade="all, delete-orphan")
    cold_water_ID = db.Column(db.Integer, db.ForeignKey('COLD_WATER.id'))
    cold_water = db.relationship("ColdWater", single_parent=True,
                              cascade="all, delete-orphan")
    other_utilities_ID = db.Column(db.Integer,
                                   db.ForeignKey('OTHER_UTILITIES.id'))
    other_utilities = db.relationship("OtherUtilities", single_parent=True,
                                   cascade="all, delete-orphan")
    sum_total = db.Column('Total Eur', db.Float)
    sent_ID = db.Column(db.Integer, db.ForeignKey('REPORT_STATUS.id'))
    sent = db.relationship("ReportStatus")


class ReportStatus(db.Model):
    __tablename__ = 'REPORT_STATUS'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), nullable=False)

    def __init__(self, status):
        self.status = status

    def __repr__(self):
        return self.status


