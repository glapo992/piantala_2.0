from app import create_app, db


app = create_app()


from app.models  import Plant_mini, Specie, Genus, Family
@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'ident':Plant_mini, 'specie':Specie,'genus':Genus, 'family':Family}