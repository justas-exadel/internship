from program_app import app, create_tables

if __name__ == "__main__":
    create_tables()
    app.run(host='127.0.0.1', port=5555, debug=True)

