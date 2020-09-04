import car


def test_car_number_add_1():
    test1 = car.Car('TTT-111')
    assert test1.car_number == 'TTT-111'
    assert test1.status == 'Successfully registered'
    assert test1.car_count == 1
    assert test1.registered_cars == 'Registered cars: TTT-111'


def test_car_number_add_2():
    test2 = car.Car('TTT-333')
    test3 = car.Car()
    test3.car_number = 'TTT-222'
    assert test3.car_number == 'TTT-222'
    assert test3.status == 'Successfully registered'
    assert test3.car_count == 2
    assert test3.registered_cars == 'Registered cars: TTT-333', 'TTT-222'

#
# def test_car_number_add_3():
#     test4 = car.Car('TTT-444')
#     test5 = car.Car()
#     test5.car_number = 'TTT-555'
#     test5.car_number = 'TTT-565'
#     assert test5.car_number == 'TTT-555'
#     assert test5.status == 'The car has already number assigned'
#     assert test5.car_count == 2
#     assert test5.registered_cars == 'Registered cars: TTT-444, TTT-555'

#
# def test_car_number_add_4():
#     test6 = car.Car('TT5-11r')
#     assert test6.car_number == None
#     assert test6.status == 'Not valid number'
#     assert test6.car_count == 0
#     assert test6.registered_cars == []
#
#
# def test_car_number_add_5():
#     test7 = car.Car()
#     test7.car_number = 'TT1-ee3'
#     assert test7.car_number == None
#     assert test7.status == 'Not valid number'
#     assert test7.car_count == 0
#     assert test7.registered_cars == []
#
#
# def test_car_number_add_6():
#     test8 = car.Car('TTT-666')
#     test9 = car.Car('TTT-666')
#     assert test9.car_number == None
#     assert test9.status == 'Already registered number'
#     assert test9.car_count == 1
#     assert test9.registered_cars == 'Registered cars: TTT-666'
#
#
# def test_car_number_del():
#     test11 = car.Car('TTT-888')
#     test10 = car.Car()
#     test10.car_number = 'TTT-777'
#     del test10
#     assert test11.car_count == 1
#     assert test11.registered_cars == 'Registered cars: TTT-888'
