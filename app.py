from flask import Flask, render_template, request, redirect, flash, url_for
import Esegui as esegui
import dataviz as dv
import os
from werkzeug.utils import secure_filename
import toDB as db
import convertImg as conv

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '.'))

UPLOAD_FOLDER = ROOT_DIR + '/static/tmp/upload/'
CONVERTED_FOLDER = ROOT_DIR + '/static/tmp/conv/'
JSON_FOLDER = ROOT_DIR + '/static/tmp/map/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'heic'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/progetto1')
def progetto1():
    return render_template('progetto1.html')


@app.route('/mappa')
def mappa():
    return render_template('mappa.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/circle_map')
def circle_map():
    '''
    Ogni volta che viene chiamato il metodo per generare la mappa,
    Questo file html viene sovrscritto con i dati nuovi
    '''
    try:
        return render_template('circle_map.html')
    except:
        return redirect(404)


@app.route('/response')
def response():

    tmplist = os.listdir(UPLOAD_FOLDER)
    imagesList = []
    convertedImagesList = []
    max = 1
    # carico solo le prime 5 foto salvate presenti in cartella
    for image in tmplist:
        if max <= 5:
            #litsa da inviare al lettore GPS
            imagePath = (UPLOAD_FOLDER + image)
            #lista da inviare alla api
            imagesList.append(UPLOAD_FOLDER + image)
            #converte immagini in jpg da inviare alla api
            convertedJpg = conv.convertJpg(imagePath)
            convertedImagesList.append(convertedJpg)
            max += 1  # Controllare se era il comportamento voluto

    #------------info da inviare al DB------------------------------------------
    # Accetta la lista di immagini e restituisce lista con lat e lon
    tagGPS = esegui.leggiGPS(imagesList=imagesList)
    # Accetta lista immaigni e restituisce un json con risposte api
    risposta = esegui.ottieniRisposta(imagesList=convertedImagesList)
    # Invio dati a firestore
    if type(risposta[1]) is float:
        db.sendCompleteData(tagGPS, risposta)
    else:
        db.sendPartialData(tagGPS, risposta)

    #------------mappa---------------------------------------------------------------
    # Crea il file JSON pullando dal database
    db.retrieveData(JSON_FOLDER)
    # Accetta un file JSON con i dati delle piante
    dv.mappa(JSON_FOLDER + 'data.json')
    # Cancella contenuto nelle cartelle tmp
    clearfolder(JSON_FOLDER)
    clearfolder(UPLOAD_FOLDER)
    clearfolder(CONVERTED_FOLDER)
    return render_template('response.html', risposta=risposta, tagGPS=tagGPS)


@app.errorhandler(404)
#
# catcha l'errore page not found e lancia la nostra pagina 404
#
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/', methods=['GET', 'POST'])
# Form: seleziona file dall'esplora risorse, puoi caricare qualsiasi tipo di file,
# questa funzione salverà in locale solo i formati accettati (ALLOWED_EXTENCTIONS)
# dopo aver salvato i file lancia response()
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
                upload = UPLOAD_FOLDER + filename
                file.save(upload)
    return redirect(url_for('response'))


#----------------------------UTILITIES--------------------------------------------


def allowed_file(filename):
    ''' verifica che il file passato abbia estensione accettata (compresa in ALLOWED_EXTENSIONS)'''
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def clearfolder(path):
    '''cancella contenuto della cartella indicata nel percorso'''
    tmplist = os.listdir(path)
    for image in tmplist:
        os.remove(path + image)


#------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
