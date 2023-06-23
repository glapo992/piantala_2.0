from flask import Flask
from config import Config
#from flask_uploads import configure_uploads, IMAGES, UploadSet


from flask_bootstrap import Bootstrap
bootstrap = Bootstrap() 

# uploads = configure_uploads()
# images = UploadSet('images', IMAGES)

def create_app(config_class = Config):
    """creation of the app istance. Allows the use of custom configuration for each istance

    :param config_class: the config for the app istance, defaults to Config
    :type config_class: Config, optional
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)
    
    #uploads.init_app(app, images)
    
    #BLUEPRINT CONFIG------------------------------
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.views import bp as views_bp
    app.register_blueprint(views_bp)

    return app