# app/admin/__init__.py

from flask import Blueprint

admin = Blueprint('admin', __name__)
user = Blueprint('user', __name__)

from . import views
