import re

class CarStatus:
    successfully_registered = 'Successfully registered'
    assigned_nuber = 'Already registered number'
    not_valid = 'Not valid number'
    number_already_is = 'The car has already number assigned'

class Car:
    registered_cars_list = []

    def __init__(self, car_number=None):
        self.status = self.car_status(car_number)
        self.has_number = False
        self.car_number = car_number
        self.car_count = self.cars_total()
        self.registered_cars = self.cars_registered()

    @property
    def car_number(self):
        return self._car_number


    @car_number.setter
    def car_number(self, number):

        if number is not None and number not in self.registered_cars_list:
            if self.is_valid(number) or self.status is None:
                self._car_number = number
                self.registered_cars_list.append(number)
                self.status = CarStatus.successfully_registered
                self.has_number = True
            else:
                self._car_number = None
        else:
            self._car_number = None

    def is_valid(self, number): #tik regex
        if number is not None:
            pattern = re.compile(r'[A-Z]{3}[-]\d{3}')
            check_reg = pattern.search(number)
            if not check_reg:
                is_valid = False
            elif number in Car.registered_cars_list:
                is_valid = False
            elif number not in Car.registered_cars_list:
                is_valid = True
        else:
            is_valid = True
        return is_valid

    def cars_registered(self):
        cars_in_string = ", ".join(self.registered_cars_list)
        return f'Registered cars: {cars_in_string}'

    def cars_total(self):
        return len(self.registered_cars_list)

    def car_status(self, number: str) -> str:
        confirmed = self.is_valid(number)
        if not confirmed:
            self.status = CarStatus.not_valid
        elif not confirmed and number in Car.registered_cars_list:
                self.status = CarStatus.assigned_nuber
        elif confirmed and number is None:
            self.status = None
        elif confirmed:
            self.status = CarStatus.successfully_registered
        else:
            self.status = None
        return self.status

    def __del__(self):
        if self.car_number in Car.registered_cars_list:
            Car.registered_cars_list.remove(self.car_number)


if __name__ == '__main__':
    # a = Car('AAA-002')
    # b = Car('BBB-002')
    # c = Car('CCC-002')
    # print(a.car_number)
    # print(a.status)
    # del a #neveikia
    # print("test", c.registered_cars)
    # print(c.car_count)
    # d = Car('CC3-002')
    # print(d.car_number)
    # print(d.registered_cars)
    # print(d.car_count)
    # print(d.status)
    e = Car()
    print(e.car_number)
    print(e.registered_cars)  # jau del suveike
    print(e.car_count)
    print(e.status)  # tipo nera ir not valid
    e.car_number = 'EEE-111' #neprideda
    print(e.car_number)
    print(type(e.registered_cars)) #jau del suveike
    print(e.car_count)
    print(e.status) #tipo nera ir not valid
    # e.car_number = 'YYY-111'
    # print(e.car_number)
    # print(e.registered_cars)
    # print(e.car_count)
    # print(e.status)