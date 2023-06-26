from app import db
from flask import render_template, flash, redirect, url_for
from app.models import Identification_mini
from app.plantnet import bp
from app.plantnet.forms import ImageForm
from utils.plantnet import manage_plant_form
#https://uiverse.io/

import os

@bp.route('/', methods = ['GET', 'POST'])
def index():   
    form = ImageForm()
    if form.validate_on_submit():
        plant = manage_plant_form(form=form)
        flash('File caricati!')
 
        return redirect(url_for('plantnet.response', plant_id = plant.id))
    return render_template('index.html' , title='Home', form = form)

@bp.route('/response/<plant_id>')
def response(plant_id):
    plant = Identification_mini.query.filter_by(id=plant_id).first()
    return render_template ('response.html', plant = plant)



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


    return render_template('response.html', risposta=risposta, tagGPS=tagGPS)"""
    


@bp.route('/about')
def about():
    return render_template('about.html', title='about us')


