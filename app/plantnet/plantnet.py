import os
import requests
import json
from app.models import Plant_mini
from config import Config
from utils.utils import clearfolder, convertJpg, exif_reader, exif_to_tag, readImg, generate_temp_folders
from app import db

# for debug only -> send a static json so the api is not called every time
from identification_sample import IDENT_FULL, IDENT_PART



def manage_plant_form(form)-> Plant_mini:
    """ Manages the form result and writes on database

    :param form: form plant upload
    :type form: FlaskForm
    :return: response view
    :rtype: view
    :return: identified plant object
    :rtype: Plant_mini
    """
    generate_temp_folders()
    filename = form.upload(Config.UPLOAD_FOLDER)# save files in temp folder
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

    #save images in store location, return relative path
    source = form.store_pics() 
    # read GPS tags
    openImg = exif_reader(files_list[0])
    tagGPS = exif_to_tag(openImg)
    #print('GPS -> ', tagGPS)

    # write on DB --> should have both files path and API response
    identfiy = Plant_mini()
    identfiy.create_plant(os.path.join(source, filename), form.organ.data, result, tagGPS)
    db.session.add(identfiy)
    db.session.commit()

    clearfolder(Config.UPLOAD_FOLDER) #clear temp folder
    clearfolder(Config.CONVERTED_FOLDER) #clear temp folder
    print('identify plant id: ', identfiy.id)
    return identfiy

def sendImg(files:list[str], organs)->list:
    """ sends file to manage the answer

    :param files: list of piscs to send
    :type files: list[str]
    :return: list API response
    :rtype: list
    """
    data = {'organs': organs}
    req = requests.Request('POST', url=Config.API_ENDPOINT, files=files, data=data)

    #! imported static json just for testing so the api is not called every time
    prepared = req.prepare()
    s = requests.Session()
    #response = s.send(prepared)
    #json_result = json.loads(response.text)
    json_result= IDENT_FULL

    #print('res compete:-->', json_result)
    list_result = plant_json_to_list(json_result)
    #print('res list:-->', list_result)
    return list_result    

def plant_json_to_list(json_result:json)-> list[str]:
    """ parse json result of api response in a usable list\n
    content of the list:\n
    specie             = result[0]\n
    reliability        = result[1]\n
    genus              = result[2]\n
    family             = result[3]\n
    common_name        = result[4]\n
    remaining_requests = result[5]

    
    :param json_result: json response form api
    :type json_result: json
    :return: list with used datas
    :rtype: list[str]
    """
    # tries to insert the value, else fills with null
    if json_result['results']:
        try:
            specie = json_result['results'][0]['species']['scientificNameWithoutAuthor'].strip()
        except:
            specie = None
        try:
            reilability = json_result['results'][0]['score']
        except:
            reilability = None
        try:
            genus = json_result['results'][0]['species']['genus'][
                'scientificNameWithoutAuthor'].strip()
        except:
            genus = None
        try:
            family = json_result['results'][0]['species']['family'][
                'scientificNameWithoutAuthor'].strip()
        except:
            family = None
        try:
            common_name = json_result['results'][0]['species']['commonNames'][0].strip()
        except:
            common_name = None
        try:
            remaining_requests = json_result['remainingIdentificationRequests']
        except:
            remaining_requests = None
        # ritorna la lista con le informazioni
        identificazione = [specie, reilability, genus, family, common_name, remaining_requests]
        return identificazione
    else:
        try:
            specie = json_result['bestMatch'].split('(')[0].strip()
        except:
            specie = None
        try:
            remaining_requests = json_result['remainingIdentificationRequests']
        except:
            remaining_requests = None
        return [specie, remaining_requests]
    


