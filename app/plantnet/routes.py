from app import db
from flask import render_template, flash, redirect, url_for, send_from_directory
from app.models import Plant_mini, Family, Genus, Specie
from app.plantnet import bp
from app.plantnet.forms import ImageForm
from app.plantnet.plantnet import manage_plant_form
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
    plant  = Plant_mini.query.filter_by(id=plant_id).first()
    print('plant specie id-> ', plant.specie_id)
    specie = Specie.query.filter_by(id=plant.specie_id).first()
    genus  = Genus.query.filter_by(id=specie.genus_id).first()
    family = Family.query.filter_by(id=genus.family_id).first()
    images_list = plant.search_specie()
    print ('image list-> ', images_list)
    
    return render_template ('response.html',title = 'response', plant = plant , specie = specie, family = family, genus = genus, images_list = images_list)

def search_specie(plant_id:int)->list[str]:
    """Returns a list plants of the same specie of the identified one"""
    plant = Plant_mini.query.filter_by(id=plant_id).first()
    images_path = Plant_mini.query.filter_by(specie=plant.specie).all()

    print('same specie paths-> ', images_path)






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
    


