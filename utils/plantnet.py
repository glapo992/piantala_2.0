import requests
import json
from config import Config


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


def sendImg(files:list[str])->list[str]:
    """ sends file to manage the answer

    :param files: list of piscs to send
    :type files: list[str]
    :return: list of fields with API response
    :rtype: lsit[str]
    """
    data = {'organs': []}
    organ = 'leaf'
    #riempie la lista organs con tanti organi 'leaf' quante foto nel ciclo
    for file in files:
        data['organs'].append(organ)

    req = requests.Request('POST', url=Config.API_ENDPOINT, files=files, data=data)

    prepared = req.prepare()
    s = requests.Session()
    response = s.send(prepared)

    json_result = json.loads(response.text)

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
