from UtilitiesCalculator.__init__ import app, db

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5555, debug=True)
    db.create_all()
