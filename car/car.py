import re


class Car:
    car_count = 0
    registered_cars = []

    def __init__(self, car_number=None):
        self.status = self.car_status(car_number)
        self.car_number = car_number

    @property
    def car_number(self):
        try:
            return self._car_number
        except AttributeError:
            return None

    @car_number.setter
    def car_number(self, number):
        if number != None and self.car_number not in self.registered_cars:
            x = self.car_status(number)
            if x == 'Successfully registered':
                self._car_number = number
                Car.registered_cars.append(self._car_number)
                Car.car_count += 1
        else:
            self.status = 'The car has already number assigned'


    def car_status(self, number: str) -> str:
        if number != None:
            pattern = re.compile(r'[A-Z]{3}[-]\d{3}')
            check_reg = pattern.search(number)
            if not check_reg:
                self.status = 'Not valid number'
            elif number in Car.registered_cars:
                self.status = 'Already registered number'
            elif number not in Car.registered_cars:
                self.status = 'Successfully registered'
        else:
            self.status = None
        return self.status

    def __del__(self):
        if self.car_number in Car.registered_cars and Car:
            Car.registered_cars.remove(self.car_number)
            Car.car_count -= 1


if __name__ == '__main__':
    a = Car('AAA-002')
    b = Car('BBB-002')
    c = Car('CCC-002')
    print(a.car_number)
    print(a.registered_cars)
    print(a.car_count)
    print(a.status)
    del a
    print("test", c.registered_cars)
    print(c.car_count)
    d = Car('CC3-002')
    print(d.car_number)
    print(d.registered_cars)
    print(d.car_count)
    print(d.status)