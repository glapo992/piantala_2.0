from flask import Flask, render_template, request, url_for, redirect
from titolo import Titolo
from plantnet import *
from Esegui import esegui

app = Flask(__name__)


#il render_template apre il file all'interno della cartella 'templates'
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/progetto1')
def progetto1():
    return render_template('progetto1.html')


@app.route('/about')
def about():
    image1 = 'static/img/piante/img1.JPG'
    image2 = 'static/img/piante/img2.JPG'
    image3 = 'static/img/piante/img3.JPG'
    image4 = 'static/img/piante/img4.JPG'
    imagesList = [image1, image2, image3, image4]

    tagGPS = esegui.leggiGPS(imagesList=imagesList)
    #risposta = esegui.ottieniRisposta(imagesList=imagesList)

    #    return render_template('about.html', risposta=risposta, tagGPS=tagGPS)
    return render_template('about.html', tagGPS=tagGPS)


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