from flask import Flask, request, jsonify
from flask_json import FlaskJSON
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import re

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

FlaskJSON(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,
                                                                    'cars.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Car_Register(db.Model):
    __tablename__ = 'car'
    id = db.Column(db.Integer, primary_key=True)
    car_number = db.Column("Car Number", db.String)
    status = db.Column("Car Status", db.String)


class NumbersDb:
    def add_to_db(self, number, status):
        db.create_all()
        added_car = Car_Register(car_number=number, status=status)
        db.session.add(added_car)
        db.session.commit()

    def check_number(self, number):
        select_car = Car_Register.query.filter_by(car_number=number).first()
        if select_car is not None:
            return True
        return False

    def registered_cars(self):
        db.create_all()
        all_cars = Car_Register.query.filter_by(
            status='Successfully registered').all()
        if Car_Register.query.filter_by(
                status='Successfully registered').count() > 0:
            car_list = [x.car_number for x in all_cars]
            cars_in_string = ", ".join(sorted(car_list))
            result = f'Registered cars: {cars_in_string}'
            return result
        else:
            result = f'There are no registered cars at this moment'
            return result

    def car_count(self):
        count_cars = Car_Register.query.filter_by(
            status='Successfully registered').count()
        return count_cars

    def delete_number(self, number):
        del_car = Car_Register.query.filter_by(car_number=number,
                                               status='Successfully registered').first()
        if del_car is not None:
            db.session.delete(del_car)
            db.session.commit()
            return True
        else:
            return False


class CarStatus:
    successfully_registered = 'Successfully registered'
    assigned_number = 'Already registered number'
    not_valid = 'Not valid number'


class Car:

    def __init__(self, car_number):
        self.status = None
        self.car_number = car_number

    @property
    def car_number(self):
        return self._car_number

    @car_number.setter
    def car_number(self, number):
        valid_number = self.is_car_number_valid(number)
        if not valid_number:
            self.status = CarStatus.not_valid
            self._car_number = number
            NumbersDb().add_to_db(number, self.status)
        else:
            number_in_db = NumbersDb().check_number(number)
            if number_in_db:
                self.status = CarStatus.assigned_number
                self._car_number = number
                NumbersDb().add_to_db(number, self.status)
            else:
                self.status = CarStatus.successfully_registered
                self._car_number = number
                NumbersDb().add_to_db(number, self.status)

    def is_car_number_valid(self, number):
        pattern = re.compile(r'[A-Z]{3}[-]\d{3}')
        validation = pattern.search(number)
        if validation is None:
            return False
        return True


@app.route('/add_car', methods=['POST'])
@limiter.limit("1/second", override_defaults=False)
def add_car():
    if request.method == 'POST':
        req_json = request.json
        number = req_json['number']
        new_car = Car(number)
        new_car_status = new_car.status
        return jsonify({f"info: {new_car_status}"})


@app.route('/registered_cars', methods=['GET'])
@limiter.limit("1/second", override_defaults=False)
def get_cars():
    result = NumbersDb().registered_cars()
    return jsonify({f"info: {result}"})


@app.route('/car_count', methods=['GET'])
@limiter.limit("1/second", override_defaults=False)
def get_car_count():
    result = NumbersDb().car_count()
    return jsonify({f"info: {result}"})


@app.route('/delete_car', methods=['DELETE'])
@limiter.limit("1/second", override_defaults=False)
def delete_cars():
    num = request.args.get('number')
    print(num)
    del_car = NumbersDb().delete_number(num)
    if del_car:
        return jsonify({"info: Deleted successfully"})
    else:
        return jsonify({"info: Can not delete this number"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
