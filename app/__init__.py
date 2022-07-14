# app/__init__.py

# third-party imports
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import abort, Flask, render_template
import psycopg2
# local imports

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config['SECRET_KEY'] = 'any secret string'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://iayfqmvcouvsof:bcd6eb5227d823e14de32cf40592db471f3e11b19eb7ce79575a4caca9f8a298@ec2-54-77-40-202.eu-west-1.compute.amazonaws.com:5432/d1e84m1vcr6itf'
    db = SQLAlchemy(app)
    Bootstrap(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"
    Migrate(app, db)
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)


    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500

    @app.route('/500')
    def error():
        abort(500)

    return app
