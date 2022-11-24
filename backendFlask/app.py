from flask import Flask, render_template, request, url_for
from titolo import Titolo
from plantnet import *
from Esegui import esegui

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
        sottotitolo=landing1.sottotitolo,
    )


#reindirizzamento alla pagina aboutus
@app.route('/about/')
def about():
    image1 = '/Users/giuliolapovich/Code/aws-azure/piantala/backendFlask/static/img/piante/img1.jpg'
    image2 = '/Users/giuliolapovich/Code/aws-azure/piantala/backendFlask/static/img/piante/img2.jpg'
    image3 = '/Users/giuliolapovich/Code/aws-azure/piantala/backendFlask/static/img/piante/img3.jpg'
    image4 = '/Users/giuliolapovich/Code/aws-azure/piantala/backendFlask/static/img/piante/img4.jpg'
    imagesList = [image1, image2, image3, image4]

    tagGPS = esegui.leggiGPS(imagesList=imagesList)
    risposta = esegui.ottieniRisposta(imagesList=imagesList)

    return render_template('about.html', risposta=risposta, tagGPS=tagGPS)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods=["GET", "POST"])
def form():
    if request.method == "POST":
        # getting input with name = lname in HTML form
        image = request.form.getlist("images")
        if len(image) > 5:
            return image[0:5]
        elif len(image) < 5:
            return image
    return render_template("form.html")


if __name__ == '__main__':
    app.run(debug=True)