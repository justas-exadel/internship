import pytest

from car import car


@pytest.fixture()
def car_number_one():
    a = car.Car('AAA-111')
    return a


@pytest.fixture()
def car_number_one_init():
    a = car.Car()
    a.car_number = 'AAA-111'
    return a


@pytest.fixture()
def car_number_two():
    a = car.Car('AAA-111')
    b = car.Car('BBB-111')
    return a, b


def test_car_number_add_1(car_number_one):
    assert car_number_one.car_number == 'AAA-111'
    assert car_number_one.status == 'Successfully registered'
    assert car_number_one.car_count == 1
    assert car_number_one.registered_cars == 'Registered cars: AAA-111'


def test_car_number_add_2(car_number_one_init):
    assert car_number_one_init.car_number == 'AAA-111'
    assert car_number_one_init.status == 'Successfully registered'
    assert car_number_one_init.car_count == 1
    assert car_number_one_init.registered_cars == 'Registered cars: AAA-111'


def test_car_number_add_3(car_number_one_init):
    car_number_one_init.car_number = 'BBB-111'
    assert car_number_one_init.car_number == 'AAA-111'
    assert car_number_one_init.status == 'The car has already number assigned'
    assert car_number_one_init.car_count == 1
    assert car_number_one_init.registered_cars == 'Registered cars: AAA-111'

def test_car_number_add_4():
    test = car.Car('TT5-11r')
    assert test.car_number == None
    assert test.status == 'Not valid number'
    assert test.car_count == 0
    assert test.registered_cars == 'There are no registered cars at this moment'


def test_car_number_add_5():
    test1 = car.Car()
    test1.car_number = 'TT1-ee3'
    assert test1.car_number == None
    assert test1.status == 'Not valid number'
    assert test1.car_count == 0
    assert test1.registered_cars == 'There are no registered cars at this moment'


def test_car_number_add_6(car_number_one):
    test2 = car_number_one
    test3 = car.Car('AAA-111')
    assert test3.car_number == None
    assert test3.status == 'Already registered number'
    assert test3.car_count == 1
    assert test3.registered_cars == 'Registered cars: AAA-111'


def test_car_number_del(car_number_one, car_number_two):
    del car_number_one
    assert car_number_two[1].car_count == 2
    assert car_number_two[1].registered_cars == 'Registered cars: AAA-111, BBB-111'






