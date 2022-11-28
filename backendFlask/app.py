from flask import Flask, render_template, request, url_for, redirect
from plantnet import *
from Esegui import esegui
from dataviz import Dataviz as dv

app = Flask(__name__)
'''il render_template apre il file all'interno della cartella templates'''


#il render_template apre il file all'interno della cartella 'templates'
@app.route('/')
def index():
    return render_template('index.html')


'''pagina vuota dimostrativa'''


@app.route('/progetto1')
def progetto1():
    return render_template('progetto1.html')


'''ogni volta che viene chiamato il metodo per generare la mappa, questo file html viene sovrscritto con i dati nuovi'''


@app.route('/circle_map')
def circle_map():
    return render_template('circle_map.html')


@app.route('/about')
def about():
    PATH='C:/Users/mc--9/Documents/ITS_Volta/IOT/Piantala/backendFlask/tmp/upload'
    tmplist = os.listdir(PATH)
    imagesList = []
    max = 1
    # carico solo le prime 5 foto salvat epresenti in cartella
    for image in tmplist:
        if max <= 5:
            imagesList.append(PATH + '/' + image)
            max + 1
    clearfolder() #elimino tutte le immagini dalla cartella
    tagGPS = esegui.leggiGPS(imagesList=imagesList)
    '''accetta lista immaigni e restituisce un json con risposte api'''
    risposta = esegui.ottieniRisposta(imagesList=imagesList)
    '''accetta file CSV con lat e lon e e specie e restituisce la mappa come oggetto html'''
    dv.mappa('fakedata.csv')
    return render_template('about.html', risposta=risposta, tagGPS=tagGPS)
    #return render_template('about.html', tagGPS=tagGPS)

    


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# #--------------------------test form------------------
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:/Users/mc--9/Documents/ITS_Volta/IOT/Piantala/backendFlask/tmp/upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'heic'}

#app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files)
        uploaded = request.files.getlist("file")
        for file in uploaded:
            print('file', file)
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload=os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(upload)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype="multipart/form-data">
      <input type=file name=file multiple="images/*">
      <input type=submit value=Upload>
    </form>
    '''
    

#-----------------------------------------------------
def clearfolder(): #delete all files in folder
    PATH='C:/Users/mc--9/Documents/ITS_Volta/IOT/Piantala/backendFlask/tmp/upload'
    tmplist = os.listdir(PATH)
    for image in tmplist:
        os.remove(PATH + '/' + image)


if __name__ == '__main__':
    app.run(debug=True)