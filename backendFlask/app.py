from flask import Flask, render_template, request, redirect, flash, url_for
import Esegui as esegui
import dataviz as dv
import os
from werkzeug.utils import secure_filename
import toDB as db

#da mettere il path relativo
UPLOAD_FOLDER = 'C:/Users/mc--9/Documents/ITS_Volta/IOT/Piantala/backendFlask/tmp/upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'heic'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/progetto1')
def progetto1():
    return render_template('progetto1.html')


@app.route('/circle_map')
#
#ogni volta che viene chiamato il metodo per generare la mappa,
# questo file html viene sovrscritto con i dati nuovi
#
def circle_map():
    return render_template('circle_map.html')


@app.route('/about')
def about():
    PATH = 'C:/Users/mc--9/Documents/ITS_Volta/IOT/Piantala/backendFlask/tmp/upload'
    tmplist = os.listdir(PATH)
    imagesList = []
    max = 1
    # carico solo le prime 5 foto salvat epresenti in cartella
    for image in tmplist:
        if max <= 5:
            imagesList.append(UPLOAD_FOLDER + image)
            max = max + 1 # Potrebbe essere una cazzata, in caso riscrivere max + 1
    #------------info da inviare al DB------------------------------------------
    '''accetta la lista di immagini e restituisce lista con lat e lon'''
    tagGPS = esegui.leggiGPS(imagesList=imagesList)
    '''accetta lista immaigni e restituisce un json con risposte api'''
    risposta = esegui.ottieniRisposta(imagesList=imagesList)
    '''invio dati a firestore'''
    if type(risposta[1]) is float:
        db.sendCompleteData(tagGPS, risposta)
    else:
        db.sendPartialData(tagGPS, risposta)
    #---------------------------------------------------------------------------
    '''accetta file CSV con lat e lon e e specie e restituisce la mappa come oggetto html'''
    dv.mappa('fakedata.csv')
    return render_template('about.html', risposta=risposta, tagGPS=tagGPS)
    #return render_template('about.html', tagGPS=tagGPS)


@app.errorhandler(404)
#
# catcha l'errore page not found e lancia la nostra pagina 404 
#
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/', methods=['GET', 'POST'])
# Form: seleziona file dall'esplora risorse, puoi caricare qualsiasi tipo di file, 
# questa funzione salverà in locale solo i formati accettati (ALLOWED_EXTENCTIONS) 
# dopo aver salvato i file lancia about() 
# al momento non gestisce nessuna eccezione
def upload_file():
    clearfolder() #elimino tutte le immagini dalla cartella
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
                upload = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(upload)
    return about()

#----------------------------UTILITIES--------------------------------------------

#
# verifica che il file passato abbia estensione accettata 
# (compresa in ALLOWED_EXTENSIONS)
#  
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#
# cancella tutti i file presenti nella cartella definita in "PATH"
#
def clearfolder():  
    PATH = 'C:/Users/mc--9/Documents/ITS_Volta/IOT/Piantala/backendFlask/tmp/upload'
    tmplist = os.listdir(PATH)
    for image in tmplist:
        os.remove(PATH + '/' + image)

#------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
