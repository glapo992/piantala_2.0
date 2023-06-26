from app import db
from flask import render_template, flash, redirect, url_for
from app.plantnet import bp
from app.plantnet.forms import ImageForm
from utils.plantnet import manage_plant_form
#https://uiverse.io/

import os


organs =[]

@bp.route('/', methods = ['GET', 'POST'])
def index():   
    form = ImageForm()
    if form.validate_on_submit():
        manage_plant_form(form=form)
        flash('File caricati!')
        return redirect(url_for('plantnet.index')) #TODO redirect to result page
    return render_template('index.html' , title='Home', form = form)



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


