import os
import requests
import json
from app.models import Identification_mini
from config import Config
from utils.utils import clearfolder, convertJpg, exif_reader, exif_to_tag, readImg
from app import db

# for debug only -> send a static json so the api is not called every time
from identification_sample import IDENT_FULL, IDENT_PART

def manage_plant_form(form):
    """ Manages the form result and write on database

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

    for file in files_list:
        jpg_file = convertJpg(file, Config.CONVERTED_FOLDER)
        jpg_image_list.append(jpg_file)                            # list with converted images
    
    # send to api jpg version of images
    files  = readImg(jpg_image_list)
    result = sendImg(files, organs=organs_list)

    #save images in store location, return path
    source = form.store_pics() 
    # read GPS tags
    openImg = exif_reader(files_list[0])
    tagGPS = exif_to_tag(openImg)
    #print('GPS -> ', tagGPS)

    # write on DB --> should have both files path and API response
    identfiy = Identification_mini()
    identfiy.create_plant(os.path.join(source, filename), form.organ.data, result, tagGPS)
    db.session.add(identfiy)
    db.session.commit()

    clearfolder(Config.UPLOAD_FOLDER) #clear temp folder
    clearfolder(Config.CONVERTED_FOLDER) #clear temp folder


def sendImg(files:list[str], organs)->list:
    """ sends file to manage the answer

    :param files: list of piscs to send
    :type files: list[str]
    :return: list API response
    :rtype: list
    """
    data = {'organs': organs}
    req = requests.Request('POST', url=Config.API_ENDPOINT, files=files, data=data)
    print(data)

    #! imported static json just for testing
    #prepared = req.prepare()
    #s = requests.Session()
    #response = s.send(prepared)
    #json_result = json.loads(response.text)
    json_result= IDENT_FULL

    #print('res compete:-->', json_result)
    list_result = plant_json_to_list(json_result)
    print('res list:-->', list_result)
    return list_result    

    

def plant_json_to_list(json_result:json)-> list[str]:
    """ parse json result of api response in a usable list

    :param json_result: json response form api
    :type json_result: json
    :return: list with used datas
    :rtype: list[str]
    """
    # Prova a inserire ogni valore, altrimenti usa un valore di default
    if json_result['results']:
        print('full ans')
        try:
            specie = json_result['results'][0]['species']['scientificName']
        except:
            specie = None
        try:
            affidabilità = json_result['results'][0]['score']
        except:
            affidabilità = None
        try:
            genus = json_result['results'][0]['species']['genus'][
                'scientificNameWithoutAuthor']
        except:
            genus = None
        try:
            family = json_result['results'][0]['species']['family'][
                'scientificNameWithoutAuthor']
        except:
            family = None
        try:
            commonName = json_result['results'][0]['species']['commonNames'][0]
        except:
            commonName = None
        try:
            remaining_requests = json_result['remainingIdentificationRequests']
        except:
            remaining_requests = None
        # ritorna la lista con le informazioni
        identificazione = [specie, affidabilità, genus, family, commonName, remaining_requests]
        return identificazione
    else:
        print('part ans')
        try:
            specie = json_result['bestMatch'].split('(')[0]
        except:
            specie = None
        try:
            remaining_requests = json_result['remainingIdentificationRequests']
        except:
            remaining_requests = None
        return [specie, remaining_requests]