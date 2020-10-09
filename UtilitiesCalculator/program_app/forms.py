from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, IntegerField,
                     SubmitField, PasswordField, SelectField)
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from wtforms_sqlalchemy.fields import QuerySelectField
from .models import User, Apartment, ServiceCost, Service, Electricity
from functools import partial
from sqlalchemy import orm
from datetime import date
from flask_login import current_user


class SignInForm(FlaskForm):
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember_psw = BooleanField("Remember me")
    submit = SubmitField('Submit')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    def validate_user(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('This email is not registered.')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirmed_psw = PasswordField('Repeat Password',
                                  validators=[DataRequired(),
                                              EqualTo(
                                                  'password')])
    submit = SubmitField('Submit')


class SignUpForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    repeated_psw = PasswordField("Repeat password",
                                 validators=[EqualTo('password',
                                                     "Passwords must match!")])
    submit = SubmitField('Submit')

    def validate(self):
        users = User.query.all()
        if users:
            raise ValidationError('User can be only one!')
        return True


class ProfileUpdateForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    submit = SubmitField('Update')

    def check_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(
                email=email.data).first()
            if user:
                raise ValidationError(
                    'This email is already taken. Choose another one.')

    def check_name(self, name):
        if name.data != current_user.name:
            user = User.query.filter_by(
                name=name.data).first()
            if user:
                raise ValidationError(
                    'This name is already taken. Choose another one.')


class GetApartments:

    def getApartment(self, columns=None):
        u = Apartment.query
        if columns:
            u = u.options(orm.load_only(*columns))
            return u

    def getApartmentFactory(self, columns=None):
        return partial(self.getApartment, columns=columns)


class GetDate:

    def getyears(self):
        x = int(date.today().strftime("%Y"))
        y = x + 1
        z = x - + 1
        list1 = [f'{z}', z]
        list2 = [f'{x}', x]
        list3 = [f'{y}', y]
        years = [tuple(list1), tuple(list2), tuple(list3)]
        return years

    def getmonths(self):
        months = []
        for i in range(1, 13):
            if len(str(i)) == 1:
                l = f"0{i}"
                months.append(tuple([f'{l}', l]))
            else:
                months.append(tuple([f'{i}', i]))
        return months

    def getcurrentmonth(self):
        current_month = int(date.today().strftime("%m"))
        current_month_indx = self.getmonths()[current_month - 2][0]
        return int(current_month_indx)


class GetElectricityData:
    def getElectricityCost(self, columns=None):
        el = Service.query.filter(Service.name == 'Electricity').first()
        u = ServiceCost.query.filter(ServiceCost.service == el)
        if columns:
            u = u.options(orm.load_only(*columns))
            return u

    def getElectricityCostFactory(self, columns=None):
        return partial(self.getElectricityCost, columns=columns)


class GetGasData:
    def getGasCost(self, columns=None):
        gas = Service.query.filter(Service.name == 'Gas').first()
        u = ServiceCost.query.filter(ServiceCost.service == gas)
        if columns:
            u = u.options(orm.load_only(*columns))
            return u

    def getGasCostFactory(self, columns=None):
        return partial(self.getGasCost, columns=columns)


class GetHotWaterData:
    def getHotWaterCost(self, columns=None):
        hw = Service.query.filter(Service.name == 'Hot Water').first()
        u = ServiceCost.query.filter(ServiceCost.service == hw)
        if columns:
            u = u.options(orm.load_only(*columns))
            return u

    def getHotWaterCostFactory(self, columns=None):
        return partial(self.getHotWaterCost, columns=columns)


class GetColdWaterData:
    def getColdWaterCost(self, columns=None):
        cw = Service.query.filter(Service.name == 'Cold Water').first()
        u = ServiceCost.query.filter(ServiceCost.service == cw)
        if columns:
            u = u.options(orm.load_only(*columns))
            return u

    def getColdWaterCostFactory(self, columns=None):
        return partial(self.getColdWaterCost, columns=columns)


class GetRentData:
    def getRentCost(self, columns=None):
        rent = Service.query.filter(Service.name == 'Rent').first()
        u = ServiceCost.query.filter(ServiceCost.service == rent)
        if columns:
            u = u.options(orm.load_only(*columns))
            return u

    def getRentCostFactory(self, columns=None):
        return partial(self.getRentCost, columns=columns)


class GetOthersData:
    def getOthersCost(self, columns=None):
        others = Service.query.filter(
            Service.name == 'Other Utilities').first()
        u = ServiceCost.query.filter(ServiceCost.service == others)
        if columns:
            u = u.options(orm.load_only(*columns))
            return u

    def getOthersCostFactory(self, columns=None):
        return partial(self.getOthersCost, columns=columns)


class UtilitiesForm(FlaskForm):
    electricity_to = IntegerField('To', validators=[DataRequired()])
    electricity_cost = QuerySelectField(
        'Cost',
        query_factory=GetElectricityData().getElectricityCostFactory(
            ['name', 'cost']),
        get_label='cost'
    )
    gas_to = IntegerField('To', validators=[DataRequired()])
    gas_cost = QuerySelectField(
        'Cost',
        query_factory=GetGasData().getGasCostFactory(['name', 'cost']),
        get_label='cost'
    )
    cold_water_to = IntegerField('To')
    cold_water_cost = QuerySelectField(
        'Cost',
        query_factory=GetColdWaterData().getColdWaterCostFactory(
            ['name', 'cost']),
        get_label='cost'
    )
    hot_water_to = IntegerField('To')
    hot_water_cost = QuerySelectField(
        'Cost',
        query_factory=GetHotWaterData().getHotWaterCostFactory(
            ['name', 'cost']),
        get_label='cost'
    )
    other_ut_cost = QuerySelectField(
        'Cost',
        query_factory=GetOthersData().getOthersCostFactory(['name', 'cost']),
        get_label='cost'
    )
    rent_cost = QuerySelectField(
        'Cost',
        query_factory=GetRentData().getRentCostFactory(['name', 'cost']),
        get_label='cost'
    )
    year = SelectField('Year', choices=GetDate().getyears(),
                       default=GetDate().getyears()[1][0])
    month = SelectField('Month', choices=GetDate().getmonths(), default=
    GetDate().getmonths()[GetDate().getcurrentmonth()][0])
    submit = SubmitField('Calculate')
    confirm = SubmitField('Confirm')


class ApartmentForm(FlaskForm):
    apartment = QuerySelectField(
        'Apartment',
        query_factory=GetApartments().getApartmentFactory(['id', 'address']),
        get_label='address'
    )
    submit = SubmitField('Select')


class GenerateReportForm(FlaskForm):
    edit = SubmitField('Edit')
    delete = SubmitField('Delete')
    pdf = SubmitField('PDF')
    send = SubmitField('SEND')
