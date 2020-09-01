import unittest
from .car import Car


class TestCars(unittest.TestCase):
    def test_car_status_succsess(self):
        test1 = Car('CCC-344')
        self.assertEqual(test1.status, 'Successfully registered')
        self.assertEqual(test1.car_number, 'CCC-344')
        self.assertEqual(test1.registered_cars, ['CCC-344'])
        self.assertEqual(test1.car_count, 1)

    def test_car_number_valid(self):
        test2 = Car('CC1-344')
        self.assertEqual(test2.status, 'Not valid number')
        self.assertEqual(test2.car_number, 'CC1-344')
        self.assertEqual(test2.registered_cars,
                         "There are no registered cars at this moment")
        self.assertEqual(test2.car_count,
                         "There are no registered cars at this moment")

    def test_car_number_already_is(self):
        test3 = Car('WWW-344')
        test4 = Car('WWW-344')
        self.assertEqual(test4.status, 'The car has already number assigned')
        self.assertEqual(test3.car_number, 'WWW-344')
        self.assertEqual(test3.registered_cars, ['WWW-344'])
        self.assertEqual(test3.car_count, 1)

    def test_car_number_already_is(self):
        test3 = Car('WWW-344')
        test4 = Car('WWW-344')
        self.assertEqual(test3.status, 'Successfully registered')
        self.assertEqual(test4.status,
                         'The car has already number assigned')  # check it
        self.assertEqual(test3.car_number, 'WWW-344')
        self.assertEqual(test3.registered_cars, ['WWW-344'])
        self.assertEqual(test3.car_count, 1)

    def test_car_number_available(self):
        test5 = Car('BBB-344')
        self.assertEqual(test5.status, 'Successfully registered')
        self.assertEqual(test5.car_number, 'BBB-344')
        self.assertEqual(test5.registered_cars, ['BBB-344'])
        self.assertEqual(test5.car_count, 1)
        test5 = Car('BBc-344')
        self.assertEqual(test5.status, 'Not valid number')
        test5 = Car('BBB-344')
        self.assertEqual(test5.status, 'The car has already number assigned')

    def test_car_counts(self):  # need fixes
        test6 = Car('AAA-344')
        self.assertEqual(test6.car_count, 1)
        test7 = Car('BBB-344')
        self.assertEqual(test7.car_count, 2)
        test8 = Car('CCC-344')
        self.assertEqual(test8.car_count, 3)

    def test_registred_car(self):  # need fixes
        test9 = Car('AAA-344')
        test10 = Car('BBB-344')
        test11 = Car('CCC-344')
        self.assertEqual(test9.registered_cars, ['AAA-344'])
        self.assertEqual(test10.registered_cars, ['AAA-344', 'BBB-344'])
        self.assertEqual(test11.registered_cars,
                         ['AAA-344', 'BBB-344', 'CCC-344'])


if __name__ == '__main__':
    unittest.main()
