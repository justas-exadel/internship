import re
from __init__ import db


class Car_Register(db.Model):
    __tablename__ = 'car'
    id = db.Column(db.Integer, primary_key=True)
    car_number = db.Column("Car Number", db.String)
    status = db.Column("Car Status", db.String)


class CarStatus:
    successfully_registered = 'Successfully registered'
    assigned_nuber = 'Already registered number'
    not_valid = 'Not valid number'
    number_already_is = 'The car has already number assigned'
    successfully_created = 'Successfully created object'


class Car:
    car_count = 0
    _registered_cars_list = []
    _car_has_number = False
    _car_status = None

    def __init__(self, car_number=None):
        self.car_number = car_number
        self.status = self._car_status

    @property
    def registered_cars(self):
        if len(Car._registered_cars_list) > 0:
            cars_in_string = ", ".join(sorted(Car._registered_cars_list))
            return f'Registered cars: {cars_in_string}'
        else:
            return 'There are no registered cars at this moment'

    def validate_status(self, number):
        if number is not None:
            if number in self._registered_cars_list:
                self._car_status = CarStatus.assigned_nuber
                return False
            elif self._car_has_number is True:
                self.status = CarStatus.number_already_is
                return False
            elif number not in self._registered_cars_list:
                pattern = re.compile(r'[A-Z]{3}[-]\d{3}')
                check_reg = pattern.search(number)
                if not check_reg and self._car_status is CarStatus.successfully_created:
                    self.status = CarStatus.not_valid
                elif not check_reg:
                    self._car_status = CarStatus.not_valid
                    return False
                elif self._car_status:
                    self.status = CarStatus.successfully_registered
                    return True
                else:
                    self._car_status = CarStatus.successfully_registered
                    return True
        else:
            self._car_status = CarStatus.successfully_created
            return False

    @property
    def car_number(self):
        return self._car_number

    @car_number.setter
    def car_number(self, number):
        validation = self.validate_status(number)
        if validation is True:
            self._car_number = number
            Car._registered_cars_list.append(number)
            Car.car_count += 1
            self._car_has_number = True
        elif validation is False and self._car_has_number is True:
            pass
        else:
            self._car_number = None

    def __del__(self):
        if self.car_number in Car._registered_cars_list and Car:
            Car._registered_cars_list.remove(self.car_number)
            Car.car_count -= 1
