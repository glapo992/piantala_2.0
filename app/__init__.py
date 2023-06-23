from flask import Flask, current_app
from config import Config


from flask_bootstrap import Bootstrap
bootstrap = Bootstrap() 


def create_app(config_class = Config):
    """creation of the app istance. Allows the use of custom configuration for each istance

    :param config_class: the config for the app istance, defaults to Config
    :type config_class: Config, optional
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)

     #BLUEPRINT CONFIG------------------------------
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.views import bp as views_bp
    app.register_blueprint(views_bp)

    return app