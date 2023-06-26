from app import db
from flask import render_template, flash, redirect, url_for, request
from app.views import bp
from app.views.forms import ImageForm
#https://uiverse.io/


from config import Config
from utils.utils import clearfolder
from utils.Esegui import ottieniRisposta, leggiGPS
from utils.convertImg import convertJpg

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
    jpg_image_list = []

    files_list.append(os.path.join(Config.UPLOAD_FOLDER,filename)) # list with original files only
    organs_list.append(form.organ.data)                            # list with selected organs of the plant
    print (files_list)

    for file in files_list:
        jpg_file = convertJpg(file, Config.CONVERTED_FOLDER)
        jpg_image_list.append(jpg_file)                             # list with converted images
    # send to api jpg version of images
    result = ottieniRisposta(jpg_image_list, organs_list)
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
   
    # check if the api returned full ans or partial only
    if len(result) == 6:
        identfiy.specie     = result[0]
        identfiy.reliability= result[1]
        identfiy.genus      = result[2]
        identfiy.family     = result[3]
        identfiy.commonName = result[4]
    else:
        identfiy.specie = result[0]
    identfiy.lat        = tagGPS[0]
    identfiy.long       = tagGPS[1]

    db.session.add(identfiy)
    db.session.commit()

    flash('File caricati!')
    clearfolder(Config.UPLOAD_FOLDER) #clear temp folder
    clearfolder(Config.CONVERTED_FOLDER) #clear temp folder

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
    


@bp.route('/about')
def about():
    return render_template('about.html', title='about us')


