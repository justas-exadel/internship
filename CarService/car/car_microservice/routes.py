from __init__ import app, db
from models import Car, Car_Register
from flask import request, jsonify


@app.route('/add_car', methods=['POST'])
def add_car():
    if request.method == 'POST':
        req_json = request.json
        number = req_json['number']
        new_car = Car(number)
        new_car_status = new_car.status
        db.create_all()
        added_car = Car_Register(car_number=number, status=new_car_status)
        db.session.add(added_car)
        db.session.commit()
        return jsonify({f"info: {new_car_status}"})


@app.route('/registered_cars', methods=['GET'])
def get_cars():
    db.create_all()
    all_cars = Car_Register.query.all()
    car_list = [x.car_number for x in all_cars]
    cars_in_string = ", ".join(sorted(car_list))
    result = f'Registered cars: {cars_in_string}'
    return jsonify({f"info: {result}"})


@app.route('/delete_car', methods=['DELETE'])
def delete_cars():
    num = request.args.get('number')
    print(num)
    del_car = Car_Register.query.filter_by(car_number=num).first()
    db.session.delete(del_car)
    db.session.commit()
    return jsonify({"info: Deleted successfully"})
