import requests
import json
from config import Config
from flask import current_app
from threading import Thread


def readImg(photos:list[str])->list:
    """ Reads a list of pics path, extract binary and retun all info in a list

    :param photos: List of pics path
    :type photos: list[str]
    :return: list of BinaryIO
    :rtype: list[str]
    """
    files = []
    if len(photos) <= 5:
        for photo in photos:
            image_data = open(photo, 'rb')
            files.append(('images', (photo, image_data)))
    return files

def send_async_data(files:list[str], data)->json:
    req = requests.Request('POST', url=Config.API_ENDPOINT, files=files, data=data)
    print(data)

    prepared = req.prepare()
    s = requests.Session()
    response = s.send(prepared)
    json_result = json.loads(response.text)
    print('async res:-->', json_result)
    return json_result


def sendImg(files:list[str], organs)->json:
    """ sends file to manage the answer

    :param files: list of piscs to send
    :type files: list[str]
    :return: json API response
    :rtype: json
    """
    data = {'organs': organs}
    
    json_result = Thread(target=send_async_data, args=(files, data)).start()
    
    return json_result



def plant_json_to_list(json_result:json)-> list[str]:
    """parse json result of api response in a usable list

    :param json_result: json response form api
    :type json_result: json
    :return: list with used datas
    :rtype: list[str]
    """
    # Prova a inserire ogni valore, altrimenti usa un valore di default
    try:
        specie = json_result['results'][0]['species']['scientificName']
    except:
        specie = 'N/D'
    try:
        affidabilità = json_result['results'][0]['score']
    except:
        affidabilità = 'N/D'
    try:
        genus = json_result['results'][0]['species']['genus'][
            'scientificNameWithoutAuthor']
    except:
        genus = 'N/D'
    try:
        family = json_result['results'][0]['species']['family'][
            'scientificNameWithoutAuthor']
    except:
        family = 'N/D'
    try:
        commonName = json_result['results'][0]['species']['commonNames'][0]
    except:
        commonName = 'N/D'
    # ritorna la lista con le informazioni
    identificazione = [specie, affidabilità, genus, family, commonName]
    return identificazione
