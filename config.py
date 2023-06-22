import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # flask general vars
    FLASK_ENV   = os.environ.get('FLASK_ENV')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    SECRET_KEY  = os.environ.get('SECRET_KEY')
    
    UPLOAD_FOLDER    = os.path.join(basedir, os.environ.get('UPLOAD_FOLDER'))
    CONVERTED_FOLDER = os.path.join(basedir, os.environ.get('CONVERTED_FOLDER'))
    JSON_FOLDER      = os.path.join(basedir, os.environ.get('JSON_FOLDER'))

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'heic'}