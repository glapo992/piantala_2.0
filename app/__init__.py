from flask import Flask
from config import Config
#from flask_uploads import configure_uploads, IMAGES, UploadSet

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_bootstrap import Bootstrap

bootstrap = Bootstrap() 

db = SQLAlchemy()    
migrate = Migrate()

def create_app(config_class = Config):
    """creation of the app istance. Allows the use of custom configuration for each istance

    :param config_class: the config for the app istance, defaults to Config
    :type config_class: Config, optional
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    
    bootstrap.init_app(app)

    
    #BLUEPRINT CONFIG------------------------------
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.plantnet import bp as plantnet_bp
    app.register_blueprint(plantnet_bp)

    return app