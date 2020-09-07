from flask import Flask, render_template, redirect, url_for
import os
import forms
from flask_sqlalchemy import SQLAlchemy

import car

app = Flask(__name__)
SECRET_KEY = os.urandom(33)
app.config['SECRET_KEY'] = SECRET_KEY
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'cars.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Car(db.Model):
    __tablename__ = 'car'
    id = db.Column(db.Integer, primary_key=True)
    car_number = db.Column("Car Number", db.String)

@app.route("/add_car", methods=['GET', 'POST'])
def add_car():
    form = forms.Car_Form()
    if form.validate_on_submit():
        db.create_all()
        car_number = form.car_number.data
        number_added = car.Car(car_number)
        new_car = Car(car_number=str(number_added.car_number))
        db.session.add(new_car)
        db.session.commit()
        return redirect(url_for('registered_cars'))
    return render_template("index.html", form=form)

@app.route("/registered_cars", methods=['GET', 'POST'])
def registered_cars():
    car_list = db.session.query(Car).all()
    return render_template("cars.html", data=car_list)

@app.route("/delete_car/number=<car_number>", methods=['GET', 'POST'])
def delete_car(car_number):
    car_obj = Car.query.filter_by(car_number=car_number).first()
    db.session.delete(car_obj)
    db.session.commit()
    return redirect(url_for('registered_cars'))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)