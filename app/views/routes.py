from app import db
from flask import render_template, flash, redirect, url_for, request
from app.views import bp
from app.views.forms import ImageForm


from config import Config
from utils.utils import clearfolder
from utils.Esegui import ottieniRisposta, leggiGPS

from app.models import Identification_mini
import os


organs =[]

@bp.route('/', methods = ['GET', 'POST'])
def index():   
    form = ImageForm()
    if form.validate_on_submit():
        plant_form(form=form)
    return render_template('index.html' , title='Home', form = form)


def plant_form(form):
    """manages the form result and write on database

    :param form: form plant upload
    :type form: FlaskForm
    :return: response view
    :rtype: view
    """
    filename = form.upload(Config.UPLOAD_FOLDER) # save files in temp folder
    # list of paths of images for the API
    files_list = [] 
    organs_list = []
    files_list.append(os.path.join(Config.UPLOAD_FOLDER,filename))
    organs_list.append(form.organ.data)
    print (files_list)
    # send to api.... 
    result = ottieniRisposta(files_list, organs_list)
    print ('result-->', result)
    source = form.store_pics() #save images in store location, return path
    # read GPS tags
    tagGPS = leggiGPS(imagesList=files_list)
    print('GPS -> ', tagGPS)
    # TODO move in another module
    # write on DB --> should have both files path and API response
    identfiy = Identification_mini()
    identfiy.img_1      = os.path.join(source, filename ) # path to the image
    identfiy.organ_1    = form.organ.data
    identfiy.reliability= result[1]
    identfiy.specie     = result[0]
    identfiy.genus      = result[2]
    identfiy.family     = result[3]
    identfiy.commonName = result[4]
    identfiy.lat        = tagGPS[0]
    identfiy.long       = tagGPS[1]
    db.session.add(identfiy)
    db.session.commit()
    flash('File caricati!')
    clearfolder(Config.UPLOAD_FOLDER) #clear temp folder
    return redirect(url_for('views.index')) #TODO redirect to result page




@bp.route('/mappa')
def mappa():
    return render_template('mappa.html',title='Mappa')


@bp.route('/circle_map')
def circle_map():
    # Rigenera l'html della mappa
    try:
        return render_template('circle_map.html')
    except:
        return redirect('errors.404', title='404')


@bp.route('/response')
def response():
    return None
"""
    # Prepara le liste per l'upload
    tmplist = os.listdir(Config.UPLOAD_FOLDER)
    imagesList = []
    convertedImagesList = []
    max = 1
    # Carico solo le prime 5 foto salvate presenti in cartella
    for image in tmplist:
        if max <= 5:
            # Lista da inviare al lettore GPS
            imagePath = (Config.UPLOAD_FOLDER + image)
            # Lista da inviare alla api
            imagesList.append(Config.UPLOAD_FOLDER + image)
            # Converte immagini in jpg da inviare alla api
            convertedJpg = conv.convertJpg(imagePath)
            convertedImagesList.append(convertedJpg)
            max += 1

    #------------info da inviare al DB------------------------------------------
    # Accetta la lista di immagini e restituisce lista con lat e lon
    tagGPS = leggiGPS(imagesList=imagesList)
    # Accetta lista immaigni e restituisce un json con risposte api
    risposta = ottieniRisposta(imagesList=convertedImagesList)
    # Invio dati a Firestore
    if type(risposta[1]) is float:
        db.sendCompleteData(tagGPS, risposta)
    else:
        db.sendPartialData(tagGPS, risposta)

    #------------mappa---------------------------------------------------------------
    # Crea il file JSON pullando dal database
    db.retrieveData(Config.JSON_FOLDER)
    # Disegna una mappa,
    # la riempie con i dati spaziali dal file json (in blu)
    # e quelli de''identificazone corrente (in rosso)
    dv.mapPlot(
        dv.circleID(tagGPS=tagGPS,
                    m=dv.mappa(Config.JSON_FOLDER + 'data.json'),
                    specie=risposta[0]))

    # Cancella contenuto nelle cartelle tmp
    clearfolder(Config.JSON_FOLDER)
    clearfolder(Config.UPLOAD_FOLDER)
    clearfolder(Config.CONVERTED_FOLDER)
    return render_template('response.html', risposta=risposta, tagGPS=tagGPS)"""
    

"""
@bp.route('/', methods=['GET', 'POST'])
# Form: seleziona file dall'esplora risorse, puoi caricare qualsiasi tipo di file,
# questa funzione salverà in locale solo i formati accettati (ALLOWED_EXTENCTIONS)
# dopo aver salvato i file lancia response()
def upload_file():
    if request.method == 'POST':
        print(request.files)
        uploaded = request.files.getlist("file")
        for file in uploaded:
            print('file', file)
            # Se l'utente non seleziona almeno un file, il browser
            # ritorna un file vuoto senza nome
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload = Config.UPLOAD_FOLDER + filename
                file.save(upload)
    return redirect(url_for('views.response'))

"""


@bp.route('/about')
def about():
    return render_template('about.html', title='about us')


