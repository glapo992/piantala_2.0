from app.models import db, datetime
from app import login
# login stuff
from flask_login import UserMixin # generic login implementations suitable for most user model classes

# pw hashing-> already provided in flask
from werkzeug.security import generate_password_hash, check_password_hash



class Users(UserMixin ,db.Model): # added UserMixin at the user class
    """ defines the User object and creates the table on the bd reflecting it"""
    id        = db.Column      (db.Integer, primary_key = True)
    username  = db.Column      (db.String(64), index = True, unique = True)
    email     = db.Column      (db.String(64), index = True, unique = True)
    pw_hash   = db.Column      (db.String(128))
    observ    = db.relationship('Plant_mini', backref = 'author', lazy = 'dynamic') # reference to the plant Model class(not table name!!), is not a db field but a view of the realtionship
    about_me  = db.Column      (db.String(150))
    last_seen = db.Column      (db.DateTime, default = datetime.utcnow)


    def set_password(self, password:str)->str:
        """generates a hash for the given pw and set it as param of the class

        :param password: hash
        :type password: str
        """
        self.pw_hash = generate_password_hash(password=password)

    def check_password(self, password:str)->bool:
        """check if the given password's hash is the same of the saved one

        :param password: passwd to check
        :type password: str
        :return: result of check
        :rtype: bool
        """
        return check_password_hash(self.pw_hash, password=password)
    

@login.user_loader
def load_user(id):
    return Users.query.get(int(id)) # querys the users id and convert into a int (only if is so saved in the databse's column)