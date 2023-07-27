from flask import Flask
from config import Config

from .extensions import db, bootstrap, migrate, login

def create_app(config_class = Config):
    """creation of the app istance. Allows the use of custom configuration for each istance

    :param config_class: the config for the app istance, defaults to Config
    :type config_class: Config, optional
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # extensions inits
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login.init_app(app)
    bootstrap.init_app(app)

    #BLUEPRINT CONFIG------------------------------
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.plantnet import bp as plantnet_bp
    app.register_blueprint(plantnet_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.user import bp as user_bp
    app.register_blueprint(user_bp)

    return app

from app import models