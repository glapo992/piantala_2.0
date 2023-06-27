from app import create_app, db


app = create_app()


from app.models  import Plant_mini
@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'idennt':Plant_mini}