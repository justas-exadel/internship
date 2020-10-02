from flask import url_for
from UtilitiesCalculator.__init__ import db
from email.message import EmailMessage
from UtilitiesCalculator.email_settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER
import smtplib
from UtilitiesCalculator.models import Electricity as El

def send_reset_email(user):
    token = user.get_reset_token()
    message = f'''
    Click the link below if you want to reset your password:
    {url_for('reset_token', token=token, _external=True)}     
     '''
    email = EmailMessage()
    email['from'] = 'Name Surname'
    email['to'] = [user.email]
    email['subject'] = 'Reset Password'

    email.set_content(message)

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        smtp.send_message(email)


class Apartment:
    def __init__(self, address, square_feet):
        self.address = address
        self.square_feet = square_feet


class House:
    def __init__(self, address):
        self.address = address
        self.apartments = list()

    def square_feet_total(self):
        return sum(a.square_feet for a in self.apartments)

    def add_apartment(self, apartment):
        self.apartments.append(apartment)

class Renter:
    def __init__(self, name, surname, email, phone):
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone

# class UtilityCategory:
#     electricity = 'Electricity'
#     gas = 'Gas'
#     hot_water = 'Hot water'
#     cold_water = 'Cold water'
#     other_utilities = 'Other utilities'
#     rent = 'Rent'

class Service:
    def __init__(self, name, cost, category):
        self.name = name
        self.cost = cost
        self.category = category


class Report:
    def __init__(self, renter, electricity, gas, hot_water, cold_water,
                 other_utilities, rent):
        self.renter = renter
        self.electricity = electricity.sum()
        self.gas = gas.sum()
        self.hot_water = hot_water.sum()
        self.cold_water = cold_water.sum()
        self.other_utilities = other_utilities.sum()
        self.rent = rent.sum()

    def sum_total(self):
        return self.electricity + self.gas + self.hot_water + self.cold_water + self.other_utilities + self.rent

