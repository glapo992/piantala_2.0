from app import db
from flask import render_template, flash, redirect, url_for, request
from app.models.plants_model import Plant_mini, Family, Genus, Specie
from app.plantnet import bp
from app.plantnet.forms import ImageForm
from app.plantnet.plantnet import manage_plant_form
from utils.dataviz import mapPlot, mappa, circleID
from flask_login import current_user
#https://uiverse.io/

import os

@bp.route('/', methods = ['GET', 'POST'])
def index():   
    form = ImageForm()
    if form.validate_on_submit():
        if current_user.is_anonymous:
            plant = manage_plant_form(form=form)
        else:
            plant = manage_plant_form(form=form, user_id=current_user.id)
        #print('routes - plant.id -> ', plant.id)
        flash('File caricati!')
        return redirect(url_for('plantnet.response', plant_id = plant.id))
    
    return render_template('index.html' , title='Piantala - Home', form = form)

@bp.route('/response/<plant_id>')
def response(plant_id):
    pl  = Plant_mini.query.filter_by(id=plant_id).first() # istance of the plant from the form
    print('plant specie_id-> ', pl.specie_id)
    sp = Specie.query.filter_by(id=pl.specie_id).first() # data from the specie of the plant
    print('retrieved genus_id -> ', sp.genus_id)
    if pl.is_complete:
        gen  = Genus.query.filter_by(id=sp.genus_id).first()
        print('retrieved genus_name-> ', gen.genus_name)
        fam = Family.query.filter_by(id=gen.family_id).first()
        print('retrieved family_name-> ', fam.family_name)
    else :
        gen  = None
        fam = None

    # list with path for the stored images of the same specie
    page = request.args.get('page', 1, type=int)
    plants_list = pl.search_specie(page)
    next_url = url_for('plantnet.response', plant_id = plant_id, page = plants_list.next_num) if plants_list.has_next else None
    prev_url = url_for('plantnet.response', plant_id = plant_id, page = plants_list.prev_num) if plants_list.has_prev else None
    #print ('image list-> ', images_list)

    coo_dict = pl.locate_specie() # dict with coordinates of other plants
    # print('coo dict -> ', coo_dict)
    # cration of the map
    mapPlot(circleID(tagGPS=[pl.lat, pl.long], m=mappa(coo_dict),tooltip=sp.specie_name) )

    return render_template ('response.html',title = 'Piantala - response', plant = pl , specie = sp, family = fam, genus = gen, plants_list = plants_list.items, next_url= next_url, prev_url= prev_url)


@bp.route('/circle_map')
def circle_map():
    """ render the template of the map """
    try:
        return render_template('_circle_map.html')
    except:
        return redirect('/404')


# display custom area on folium map   
# https://gis.stackexchange.com/questions/378431/mapping-multiple-polygons-on-folium

