from __init__ import app, db
from models import Service

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5555, debug=True)
    db.create_all()
    electricity = Service(name='Electricity')
    gas = Service(name='Gas')
    hot_water = Service(name='Hot Water')
    cold_water = Service(name='Cold Water')
    rent = Service(name='Rent')
    others = Service(name='Other Utilities')
    db.session.add(electricity)
    db.session.add(gas)
    db.session.add(hot_water)
    db.session.add(cold_water)
    db.session.add(rent)
    db.session.add(others)
    db.session.commit()
