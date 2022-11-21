from flask import Flask
from flask import render_template

#al momento non ha altro che caricare una pagina bianca che reindirizza a un url di una pagina già hostata su firebase

app = Flask(__name__)


#app.route conduce a una pagina html bianca salvata in flask che non fa niente.
#il return fa il redirect a firebase
@app.route('/')
def index():
    return render_template('index.html')
