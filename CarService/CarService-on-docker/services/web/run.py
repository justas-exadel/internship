from project import app, limiter, db

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

#host='127.0.0.1' if you want run not on docker

