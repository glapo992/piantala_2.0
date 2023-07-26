from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_bootstrap import Bootstrap
from flask_login import LoginManager 

bootstrap = Bootstrap() 

db = SQLAlchemy()    
migrate = Migrate()

login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'eseguire il login per accedere questa pagina'