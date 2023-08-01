from app import create_app
from app.extensions import db

app = create_app()


from app.models.plants_model  import Plant_mini, Specie, Genus, Family
from app.models.user_model import Users
@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'ident':Plant_mini, 'specie':Specie,'genus':Genus, 'family':Family}