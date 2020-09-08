import re
from __init__ import db


class Car_Register(db.Model):
    __tablename__ = 'car'
    id = db.Column(db.Integer, primary_key=True)
    car_number = db.Column("Car Number", db.String)
    status = db.Column("Car Status", db.String)


class CarStatus:
    successfully_registered = 'Successfully registered'
    assigned_number = 'Already registered number'
    not_valid = 'Not valid number'
    number_already_is = 'The car has already number assigned'
    successfully_created = 'Successfully created object'


class Car:
    _registered_cars = []

    def __init__(self, car_number=None):
        self.status = None
        self._car_has_number = False
        self.car_number = car_number

    @property
    def registered_cars(self):
        if len(self._registered_cars) > 0:
            car_string = ", ".join(sorted(self._registered_cars))
            return f'Registered cars: {car_string}'
        else:
            return 'There are no registered cars at this moment'

    @property
    def car_count(self):
        return len(self._registered_cars)

    @property
    def car_number(self):
        return self._car_number

    @car_number.setter
    def car_number(self, number):
        if number is None:
            self._car_number = None
            self.status = CarStatus.successfully_created
        else:
            valid_number = self.is_car_number_valid(number)

            if not valid_number:
                self.status = CarStatus.not_valid
                self._car_number = None

            else:  # car_number is not None and car_number is valid
                if number in self._registered_cars:
                    self.status = CarStatus.assigned_number
                    if not self._car_has_number:
                        self._car_number = None
                else:
                    if self._car_has_number:
                        self.status = CarStatus.number_already_is
                    else:
                        self.status = CarStatus.successfully_registered
                        self._car_number = number
                        self._registered_cars.append(number)
                        self._car_has_number = True

    def is_car_number_valid(self, number):
        pattern = re.compile(r'[A-Z]{3}[-]\d{3}')
        validation = pattern.search(number)
        if validation is None:
            return False
        return True

    def __del__(self):
        if self.car_number in self._registered_cars:
            self._registered_cars.remove(self.car_number)