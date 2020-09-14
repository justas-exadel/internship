from . import app, db, limiter
from project.models import Car, Car_Register, NumbersDb
from flask import request, jsonify


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
    del_car = NumbersDb().delete_number(num)
    if del_car:
        return jsonify({"info: Deleted successfully"})
    else:
        return jsonify({"info: Can not delete this number"})

