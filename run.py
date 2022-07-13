# run.py
import os
from app import create_app


config_name = os.getenv('SQLALCHEMY_DATABASE_URI', 'default')
app = create_app(config_name)


if __name__ == '__main__':
    app.run(host='localhost', port=5000)