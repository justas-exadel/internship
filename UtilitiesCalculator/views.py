import os
import smtplib
from email.message import EmailMessage
from flask import render_template, redirect, url_for, flash, request, \
    make_response
from forms import SignInForm, SignUpForm, PasswordResetForm, UtilitiesForm, \
    RequestResetForm, ProfileUpdateForm, ApartmentForm, GenerateReportForm
from flask_paginate import Pagination, get_page_args
from flask_login import logout_user, login_user, login_required
from flask_login import current_user
from __init__ import app, db, bcrypt, login_manager
from models import Electricity, Gas, HotWater, ColdWater, Rent, OtherUtilities, \
    User, Report, Apartment
from sqlalchemy import asc, desc
import pdfkit


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
    db.create_all()
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


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileUpdateForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile is updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    return render_template('profile.html', title='Account', form=form)


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


@app.route("/select_apartment", methods=['GET', 'POST'])
@login_required
def select_apartment():
    apartment_form = ApartmentForm()
    if apartment_form.validate_on_submit():
        apartment = apartment_form.apartment.data
        return redirect(url_for('calculate_utilities', apartment=apartment.id))
    return render_template('select_apartment.html',
                           apartment_form=apartment_form)


class GetFromData:
    def __init__(self, service, apartment):
        self.service = service
        self.apartment = apartment

    def getFrom(self):
        try:
            last = \
                self.service.query.filter_by(
                    apartment_ID=self.apartment).order_by(
                    asc(self.service.id)).all()[-1]
            data_from = last.consumption_to
            return data_from
        except IndexError:
            return 0


def data_to_db(*data):
    for ut in data:
        db.session.add(ut)
    db.session.commit()


def calculate_from(apartment):
    electricity_from = GetFromData(Gas, apartment).getFrom()
    gas_from = GetFromData(Gas, apartment).getFrom()
    hot_water_from = GetFromData(HotWater, apartment).getFrom()
    cold_water_from = GetFromData(ColdWater, apartment).getFrom()
    data_from_last = {
        "electricity_from": electricity_from,
        "gas_from": gas_from,
        "hot_water_from": hot_water_from,
        "cold_water_from": cold_water_from
    }
    return data_from_last


def result_data(electricity_dif, gas_dif, cold_water_dif, hot_water_dif,
                electricity_sum, gas_sum, cold_water_sum, hot_water_sum,
                other_ut_sum, rent_sum, total_sum):
    data = {
        'electricity_dif': electricity_dif,
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
    return data


def calculate_data(electricity_to, electricity_from, gas_to, gas_from,
                   cold_water_to, cold_water_from, hot_water_to,
                   hot_water_from, electricity_cost, gas_cost, cold_water_cost,
                   hot_water_cost, others_cost, rent_cost):
    electricity_dif = electricity_to - electricity_from
    print("ss", electricity_from)
    gas_dif = gas_to - gas_from
    cold_water_dif = cold_water_to - cold_water_from
    hot_water_dif = hot_water_to - hot_water_from

    electricity_sum = round(electricity_dif * electricity_cost, 2)
    gas_sum = round(gas_dif * gas_cost, 2)
    cold_water_sum = round(cold_water_dif * cold_water_cost, 2)
    hot_water_sum = round(hot_water_dif * hot_water_cost, 2)
    other_ut_sum = others_cost
    rent_sum = rent_cost
    total_sum = round(
        electricity_sum + gas_sum + cold_water_sum + hot_water_sum + other_ut_sum + rent_sum,
        2)

    data = result_data(electricity_dif, gas_dif, cold_water_dif,
                       hot_water_dif, electricity_sum, gas_sum,
                       cold_water_sum, hot_water_sum, other_ut_sum,
                       rent_sum, total_sum)
    return data


@app.route("/calculate_utilities/<apartment>", methods=['GET', 'POST'])
@login_required
def calculate_utilities(apartment):
    db.create_all()
    form = UtilitiesForm()
    data_from_last = calculate_from(apartment)
    if form.validate_on_submit():
        if 'confirm' in request.form:
            el_db = Electricity(year=form.year.data, month=form.month.data,
                                consumption_from=int(
                                    request.form['electricity_from']),
                                consumption_to=form.electricity_to.data,
                                difference=request.form['electricity_dif'],
                                apartment_ID=apartment,
                                cost=form.electricity_cost.data,
                                sum=request.form['electricity_sum'])

            gas_db = Gas(year=form.year.data, month=form.month.data,
                         consumption_from=int(request.form['gas_from']),
                         consumption_to=form.gas_to.data,
                         difference=request.form['gas_dif'],
                         apartment_ID=apartment,
                         cost=form.gas_cost.data,
                         sum=request.form[
                             'gas_sum'])

            hot_water_db = HotWater(year=form.year.data, month=form.month.data,
                                    consumption_from=int(
                                        request.form['hot_water_from']),
                                    consumption_to=form.hot_water_to.data,
                                    difference=request.form['hot_water_dif'],
                                    apartment_ID=apartment,
                                    cost=form.hot_water_cost.data,
                                    sum=request.form[
                                        'hot_water_sum'])

            cold_water_db = ColdWater(year=form.year.data,
                                      month=form.month.data,
                                      consumption_from=int(
                                          request.form['cold_water_from']),
                                      consumption_to=form.cold_water_to.data,
                                      difference=request.form[
                                          'cold_water_dif'],
                                      apartment_ID=apartment,
                                      cost=form.cold_water_cost.data,
                                      sum=request.form[
                                          'cold_water_sum'])
            others_db = OtherUtilities(year=form.year.data,
                                       month=form.month.data,
                                       apartment_ID=apartment,
                                       cost=form.other_ut_cost.data,
                                       sum=request.form[
                                           'other_ut_sum'])

            rent_db = Rent(year=form.year.data, month=form.month.data,
                           apartment_ID=apartment,
                           cost=form.rent_cost.data,
                           sum=request.form[
                               'rent_sum'])

            report = Report(rent=rent_db, electricity=el_db, gas=gas_db,
                            hot_water=hot_water_db, cold_water=cold_water_db,
                            other_utilities=others_db,
                            sum_total=request.form['total_sum'], sent_ID=2)

            data_to_db(el_db, gas_db, hot_water_db, cold_water_db, others_db,
                       rent_db, report)

            flash(
                f'Utilities data is successfully saved!',
                'success')
            return redirect("/select_apartment")

        data = calculate_data(form.electricity_to.data,
                              int(request.form['electricity_from']),
                              form.gas_to.data, int(request.form['gas_from']),
                              form.cold_water_to.data,
                              int(request.form['cold_water_from']),
                              form.hot_water_to.data,
                              int(request.form['hot_water_from']),
                              form.electricity_cost.data.cost,
                              form.gas_cost.data.cost,
                              form.cold_water_cost.data.cost,
                              form.hot_water_cost.data.cost,
                              form.other_ut_cost.data.cost,
                              form.rent_cost.data.cost)

        return render_template('calculate_utilities.html', form=form,
                               data=data, data_from_last=data_from_last,
                               apartment_selected=Apartment.query.filter_by(
                                   id=apartment).first())

    return render_template('calculate_utilities.html', form=form,
                           data_from_last=data_from_last,
                           apartment_selected=Apartment.query.filter_by(
                               id=apartment).first())


@app.route('/generate_report', methods=['GET', 'POST'])
@login_required
def generate_report():
    data = Report.query.filter_by(sent_ID=2).all()
    return render_template('reports.html', data=data)


@app.route('/reports_history', methods=['GET', 'POST'])
@login_required
def reports_history():
    data = Report.query.order_by(desc(Report.id)).all()
    return render_template('reports_history.html', data=data)


@app.route("/report/<id>/view", methods=['GET', 'POST'])
@login_required
def generated_report(id):
    form = GenerateReportForm()
    report = Report.query.filter_by(id=id).first()
    if form.validate_on_submit():
        if 'edit' in request.form:
            return redirect(url_for('edit_report', id=id))
        elif 'pdf' in request.form:
            return redirect(url_for('report_pdf', id=id))
        elif 'send' in request.form:
            return redirect(url_for('send_report', id=id))
        elif 'delete' in request.form:
            return redirect(
                url_for('delete_report', id=report.id))

    return render_template('generated_report.html', report=report, form=form)


@app.route('/report/<id>')
@login_required
def report_pdf(id):
    name = "Generated Report"
    report = Report.query.filter_by(id=id).first()
    html = render_template('report_pdf.html', name=name, report=report)
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers[
        'Content-Disposition'] = f'attachement; filename=utilities_report_{id}.pdf'
    return response


def get_latest_pdf(path):
    files = os.listdir(path)
    latest = files[0]
    for key in files:
        if os.path.getctime(path + key) > os.path.getctime(path + latest):
            latest = key
    return latest


def change_report_status(id):
    Report.query.filter_by(id=id).update(dict(sent_ID=1))
    db.session.commit()


@app.route('/send_report/<id>')
@login_required
def send_report(id):
    message = '''
        Dear Sir/Madam,
        Please find attached report about your rent and utilities month consumption.
        Sincerely,
        Landlord
        '''
    email = EmailMessage()
    email['from'] = 'Apartment Rent'
    email['to'] = 'viskoniekas@gmail.com'
    email['subject'] = 'utilities consumption report'

    email.set_content(message)
    os.chdir(
        'C:\\Users\\GertrudaSK\\Downloads')
    report = get_latest_pdf('C:/Users/GertrudaSK/Downloads/')

    with open(f'{report}', 'rb') as file:
        content = file.read()
        email.add_attachment(
            content,
            maintype='application/pdf',
            subtype='pdf',
            filename=f'{report}')

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('viskoniekas@gmail.com', 'XXX')
        smtp.send_message(email)
        change_report_status(id)
    flash(
        f'Report is successfully sent!',
        'success')
    return redirect("/generate_report")


@app.route('/report/<id>/update', methods=['GET', 'POST'])
@login_required
def edit_report(id):
    report = Report.query.filter_by(id=id).first()
    form = UtilitiesForm(request.form)
    if form.validate_on_submit():
        if 'confirm' in request.form:
            report.electricity.consumption_to = form.electricity_to.data
            report.electricity.cost = form.electricity_cost.data
            report.electricity.difference = request.form['electricity_dif']
            report.electricity.sum = request.form['electricity_sum']

            report.gas.consumption_to = form.gas_to.data
            report.gas.cost = form.gas_cost.data
            report.gas.difference = request.form['gas_dif']
            report.gas.sum = request.form['gas_sum']

            report.cold_water.consumption_to = form.cold_water_to.data
            report.cold_water.cost = form.cold_water_cost.data
            report.cold_water.difference = request.form['cold_water_dif']
            report.cold_water.sum = request.form['cold_water_sum']

            report.hot_water.consumption_to = form.hot_water_to.data
            report.hot_water.cost = form.hot_water_cost.data
            report.hot_water.difference = request.form['hot_water_dif']
            report.hot_water.sum = request.form['hot_water_sum']

            report.other_utilities.cost = form.other_ut_cost.data
            report.rent.cost = form.rent_cost.data
            report.sum_total = request.form['total_sum']
            db.session.commit()
            flash('Report updated successfully!', 'success')
            return redirect(url_for('generated_report', id=id))
        elif 'submit' in request.form:
            data = calculate_data(form.electricity_to.data,
                                  report.electricity.consumption_from,
                                  form.gas_to.data,
                                  report.gas.consumption_from,
                                  form.cold_water_to.data,
                                  report.cold_water.consumption_from,
                                  form.hot_water_to.data,
                                  report.hot_water.consumption_from,
                                  form.electricity_cost.data.cost,
                                  form.gas_cost.data.cost,
                                  form.cold_water_cost.data.cost,
                                  form.hot_water_cost.data.cost,
                                  form.other_ut_cost.data.cost,
                                  form.rent_cost.data.cost)

            return render_template('edit_report.html', form=form,
                                   data=data, report=report)

    form.electricity_to.data = report.electricity.consumption_to
    form.electricity_cost.data = report.electricity.cost
    form.gas_to.data = report.gas.consumption_to
    form.gas_cost.data = report.gas.cost
    form.cold_water_to.data = report.cold_water.consumption_to
    form.cold_water_cost.data = report.cold_water.cost
    form.hot_water_to.data = report.hot_water.consumption_to
    form.hot_water_cost.data = report.hot_water.cost
    form.other_ut_cost.data = report.other_utilities.cost
    form.other_ut_cost.data = report.other_utilities.cost
    form.other_ut_cost.data = report.other_utilities.cost
    form.rent_cost.data = report.rent.cost
    return render_template('edit_report.html', form=form, report=report)


@app.route('/report/<id>/delete', methods=['GET', 'POST'])
@login_required
def delete_report(id):
    report = Report.query.filter_by(id=id).first()
    db.session.delete(report)
    db.session.commit()
    flash('The report has been deleted!', 'success')
    return redirect(url_for('home'))
