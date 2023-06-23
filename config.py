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

    try:
        PASSWORD = os.environ.get('DB_PASSWORD') 
        USERNAME = os.environ.get('DB_USERNAME') 
        HOST     = os.environ.get('DB_HOST') 
        DB_NAME  = os.environ.get('DB_DB_NAME') 

        if USERNAME and PASSWORD and HOST and DB_NAME:
            db_url = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}/{DB_NAME}"
        else:
            raise KeyError('Some necessary environment variable(s) are not defined')
        SQLALCHEMY_DATABASE_URI = db_url
    except:  
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+ os.path.join(basedir, 'app.db') # reading config. if no path to db, it creates one in the basedir
        SQLALCHEMY_TRACK_MODIFICATIONS = False