import re
import inspect

callers = []
cars_list = []


class Car:
    caller = ""
    count = 0

    def __init__(self, car_number):
        call_name = str(inspect.stack()[1][4]).split()[0][2:]
        self.caller = call_name
        self.car_number = car_number
        self.status = self.car_status(car_number)
        self.registered_cars = self.car_registred()
        self.car_count = self.cars_count()  # gives bad count

    def getInstanceName(self):
        return self.caller

    def car_status(self, number: str) -> str:
        pattern = re.compile(r'[A-Z]{3}[-]\d{3}')
        check_reg = pattern.search(number)
        if not check_reg:
            self.status = 'Not valid number'
        elif self.caller in callers:
            self.status = 'The car has already number assigned'
        elif number in cars_list:
            self.status = 'Already registered number'
        elif number not in cars_list and check_reg and self.caller not in callers:
            self.status = 'Successfully registered'
            cars_list.append(number)
            callers.append(self.caller)
            Car.count += 1
        return self.status

    def car_registred(self):
        if len(cars_list) == 0:
            self.registered_cars = "There are no registered cars at this moment"
        else:
            self.registered_cars = cars_list
        return self.registered_cars

    def cars_count(self):
        if len(cars_list) == 0:
            self.car_count = "There are no registered cars at this moment"
        else:
            self.car_count = Car.count
        return self.car_count

    def __del__(self):
        if self.car_number in cars_list and Car:
            cars_list.remove(self.car_number)
            Car.count -= 1


if __name__ == '__main__':
    c = Car('CCC-344')
    print(c.status)
    print(c.car_number)
    print(c.registered_cars)
    print(c.car_count)
