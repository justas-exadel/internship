from flask import url_for
from __init__ import db
from email.message import EmailMessage
from email_settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER
import smtplib
from models import Electricity as El

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

