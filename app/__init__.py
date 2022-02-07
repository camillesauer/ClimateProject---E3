# app/__init__.py
from main import mysql_connect
# third-party imports
from flask import Flask

# local imports
from config import app_config

# db variable initialization
app = Flask(__name__)
db = mysql_connect()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    return app

def create_app(config_name):
    # existing code remains

    # temporary route
    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    return app