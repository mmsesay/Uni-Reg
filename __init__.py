#!/usr/bin/python3
# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import make_response, abort, jsonify
from flask_cors import CORS

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    """This function creates the app and instantiates the 
    blueprints."""
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    # conn = 'postgresql://maej:maejor123@localhost/ziidb'
    app.config['SECRET_KEY'] = 'USL232'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sl_uni.db?check_same_thread=False'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CORS_HEADERS'] = 'Content-Type/json'

    # instantiating the app
    db.init_app(app)

    # creating a LoginManager object
    login_manager = LoginManager()
    login_manager.login_view = 'fbc.Login'
    login_manager.init_app(app)

    # importing the models
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for fbc's routes in app
    from .fbc import fbc as fbc_blueprint
    app.register_blueprint(fbc_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
