from flask import render_template, redirect, url_for, flash, request
from UtilitiesCalculator.forms import SignInForm, RequestResetForm, PasswordResetForm, SignUpForm
from flask_paginate import Pagination, get_page_args
from flask_login import logout_user, login_user, login_required
import secrets
import smtplib
from email.message import EmailMessage
from flask_login import current_user
import os
from UtilitiesCalculator.__init__ import app, db, bcrypt, login_manager
from UtilitiesCalculator.models import User
from UtilitiesCalculator.email_settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER

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
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember_psw.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(
                url_for('home'))
        else:
            flash('Email or password is not correct',
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