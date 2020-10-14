from app import app, db, database_initialization_sequence, admin_create

import os
from os.path import join, dirname

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')  # Address of your .env file
load_dotenv(dotenv_path)


config_name = os.getenv('FLASK_CONFIG')

if __name__ == "__main__":
    db.create_all()
    database_initialization_sequence()
    admin_create()
    app.run(debug=True, host='0.0.0.0')
    # app.run(host='127.0.0.1', port=5555, debug=True)

