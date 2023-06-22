from flask import Blueprint

# istance of the blueprint obj:
# name of the blueprint, name of the base module (__name__), template_folder= name of the folder where template are stored 
bp = Blueprint('views',__name__, template_folder='templates')

from app.views import routes