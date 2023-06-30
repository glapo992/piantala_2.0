import os

class Config(object):
    # flask general vars
    BASEDIR     = os.path.abspath(os.path.dirname(__file__))
    FLASK_ENV   = os.environ.get('FLASK_ENV')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    SECRET_KEY  = os.environ.get('SECRET_KEY')

    try:
        UPLOAD_FOLDER    = os.path.join(BASEDIR, os.environ.get('UPLOAD_FOLDER') )
        CONVERTED_FOLDER = os.path.join(BASEDIR, os.environ.get('CONVERTED_FOLDER'))
        JSON_FOLDER      = os.path.join(BASEDIR, os.environ.get('JSON_FOLDER'))
    except:
        UPLOAD_FOLDER    = '.'
        CONVERTED_FOLDER = '.'
        JSON_FOLDER      = '.'



    PROJECT = os.environ.get('PROJECT')
    PLANTNET_API_KEY = os.environ.get('PLANTNET_API_KEY') 
    API_ENDPOINT = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={PLANTNET_API_KEY}"  #url a cui fare la richiesta

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'heic'}

    CODEC = 'ISO-8859-1'  # or latin-1, serve a decodificare i tag exif

    IMG_PER_PAGE = 10

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
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+ os.path.join(BASEDIR, 'app.db') # reading config. if no path to db, it creates one in the BASEDIR
        SQLALCHEMY_TRACK_MODIFICATIONS = False