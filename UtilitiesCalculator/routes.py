from flask import render_template, redirect, url_for, flash, request
from UtilitiesCalculator.forms import SignInForm, SignUpForm, PasswordResetForm, UtilitiesForm, RequestResetForm
from flask_paginate import Pagination, get_page_args
from flask_login import logout_user, login_user, login_required
import secrets
from flask_login import current_user
import os
from UtilitiesCalculator.__init__ import app, db, bcrypt, login_manager
from UtilitiesCalculator.models import User
from UtilitiesCalculator.main import send_reset_email
from UtilitiesCalculator.models import Electricity, Gas, HotWater, ColdWater, Rent, OtherUtilities

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    try:
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            user = User(name=form.name.data,
                                    email=form.email.data,
                                    password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Successfully signed up!', 'success')
            return redirect(url_for('home'))
        return render_template('sign_up.html', title='Register', form=form)
    except Exception:
        flash('User can be only one!', 'danger')
        return redirect(url_for('sign_up'))


@app.route("/sign_in", methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignInForm()
    user = User.query.filter_by(email=form.email.data).first()
    if form.validate_on_submit():
        if user:
            if user and bcrypt.check_password_hash(user.password,
                                                   form.password.data):
                login_user(user, remember=form.remember_psw.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(
                    url_for('home'))
            else:
                flash('Email or password is not correct',
                      'danger')
        else:
            flash('This user is not registered',
                  'danger')
    return render_template('sign_in.html', title='Sign In', form=form)

@app.route("/sign_out")
@login_required
def sign_out():
    logout_user()
    return render_template('index.html')

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            send_reset_email(user)
            flash(
                'The new password link is already sent to your email!', 'info')
            return redirect(url_for('sign_in'))
        except Exception:
            flash('This email is not registered', 'danger')
            return redirect(url_for('reset_request'))
    return render_template('reset_request.html', title='Reset Password',
                           form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('This link is no longer valid ', 'warning')
        return redirect(url_for('reset_request'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password is changed successfully', 'success')
        return redirect(url_for('sign_in'))
    return render_template('reset_token.html', title='Reset Password',
                           form=form)


@app.route("/calculate_utilities", methods=['GET', 'POST'])
@login_required
def calculate_utilities():
    db.create_all()
    form = UtilitiesForm()
    if form.validate_on_submit():
        if 'confirm' in request.form:
            el_db = Electricity(year=form.year.data, month=form.month.data, consumption_from=form.electricity_from.data, consumption_to=form.electricity_to.data,
                 difference=request.form['electricity_dif'], apartment=form.apartment.data, cost=form.electricity_cost.data, sum=request.form['electricity_sum'])

            gas_db = Gas(year=form.year.data, month=form.month.data,
                                consumption_from=form.gas_from.data,
                                consumption_to=form.gas_to.data,
                                difference=request.form['gas_dif'],
                                apartment=form.apartment.data,
                                cost=form.gas_cost.data,
                                sum=request.form[
                                    'gas_sum'])

            hot_water_db = HotWater(year=form.year.data, month=form.month.data,
                         consumption_from=form.hot_water_from.data,
                         consumption_to=form.hot_water_to.data,
                         difference=request.form['hot_water_dif'],
                         apartment=form.apartment.data,
                         cost=form.hot_water_cost.data,
                         sum=request.form[
                             'hot_water_sum'])

            cold_water_db = ColdWater(year=form.year.data, month=form.month.data,
                         consumption_from=form.cold_water_from.data,
                         consumption_to=form.cold_water_to.data,
                         difference=request.form['cold_water_dif'],
                         apartment=form.apartment.data,
                         cost=form.cold_water_cost.data,
                         sum=request.form[
                             'cold_water_sum'])
            others_db =  OtherUtilities(year=form.year.data, month=form.month.data,
                         apartment=form.apartment.data,
                         cost=form.other_ut_cost.data,
                         sum=request.form[
                             'other_ut_sum'])

            rent_db =  Rent(year=form.year.data, month=form.month.data,
                         apartment=form.apartment.data,
                         cost=form.rent_cost.data,
                         sum=request.form[
                             'rent_sum'])

            db.session.add(el_db)
            db.session.add(gas_db)
            db.session.add(hot_water_db)
            db.session.add(cold_water_db)
            db.session.add(others_db)
            db.session.add(rent_db)
            db.session.commit()

        electricity_dif = form.electricity_to.data - form.electricity_from.data
        gas_dif = form.gas_to.data - form.gas_from.data
        cold_water_dif = form.cold_water_to.data - form.cold_water_from.data
        hot_water_dif =  form.hot_water_to.data -  form.hot_water_from.data

        electricity_sum = round(electricity_dif * form.electricity_cost.data, 2)
        gas_sum = round(gas_dif * form.gas_cost.data, 2)
        cold_water_sum = round(cold_water_dif * form.cold_water_cost.data, 2)
        hot_water_sum =  round(hot_water_dif *  form.hot_water_cost.data, 2)
        other_ut_sum = form.other_ut_cost.data
        rent_sum = form.rent_cost.data
        total_sum = electricity_sum + gas_sum + cold_water_sum + hot_water_sum + other_ut_sum + rent_sum

        data = {
            'electricity_dif':  electricity_dif,
            'gas_dif': gas_dif,
            'cold_water_dif': cold_water_dif,
            'hot_water_dif': hot_water_dif,
            'electricity_sum': electricity_sum,
            'gas_sum': gas_sum,
            'cold_water_sum': cold_water_sum,
            'hot_water_sum': hot_water_sum,
            'other_ut_sum': other_ut_sum,
            'rent_sum': rent_sum,
            'total_sum': total_sum
        }
        return render_template('calculate_utilities.html', form=form, data=data)

    return render_template('calculate_utilities.html', form=form)



