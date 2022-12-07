import requests
import json

API_KEY = "2b10vOWpgAoY62YLF1X5UiDzu"  # API_KEY dal mio account plantNet
PROJECT = "weurope"  #identifica la zona di interesse in cui fare la ricerca
api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"  #url a cui fare la richiesta


def readImg(photos):
    '''
    Questa funzione deve leggere la lista di foto in entrata, e per ogni elemento estrarre il binario (con 'rb') salvato in img_data
    poi deve riempire la lista 'file' con il path dell'immagine e relativo bianrio
    il limite delle 5 foto lo mettiamo qui o nel form html? o entrambi?
    
    Parameters
    ---
    photos : list[str]
        Lista di path delle foto

    Returns
    ---
    files : list
        Lista di BinaryIO
    '''
    files = []
    if len(photos) <= 5:
        for photo in photos:
            image_data = open(photo, 'rb')
            files.append(('images', (photo, image_data)))
    return files


def sendImg(files):
    '''
    Gestisce l'invio dei file a Pl@ntNET e la risposta dell'IA.
    
    Parameters:
    ---
    files : list
        Lista dei path delle immagini da mandare

    Returns:
    ---
    identificazione : list
        Lista con i campi ottenuti dal riconoscimento
    '''
    data = {'organs': []}
    organ = 'leaf'
    for file in files:  #riempie la lista organs con tanti organi 'leaf' quante foto nel ciclo
        data['organs'].append(organ)

    req = requests.Request('POST', url=api_endpoint, files=files, data=data)

    prepared = req.prepare()
    s = requests.Session()
    response = s.send(prepared)

    json_result = json.loads(response.text)

    # prova a inserire ogni valore, altrimenti usa un valore di default
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
