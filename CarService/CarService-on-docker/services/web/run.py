from project import app, limiter, db

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(host='127.0.0.1', port=5555, debug=True)


