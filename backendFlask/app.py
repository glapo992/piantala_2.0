from flask import Flask, render_template
from titolo import Titolo

app = Flask(__name__)


#il render_template apre il file all'interno della cartella 'templates'
@app.route('/')
def index():
    #titolo dinamico fatto solo per vedere come funziona jinja e oggetti in py
    landing1 = Titolo('piantala', 'di rompere il cazzo')
    return render_template(
        'index.html',
        #rimuovere questa parte sotto e il landing1
        titolo_princ=landing1.primo_titolo,
        sottotitolo=landing1.sottotitolo)


#reindirizzamento alla pagina aboutus
@app.route('/about/')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
