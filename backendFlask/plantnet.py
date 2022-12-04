import requests
import json

API_KEY = "2b10vOWpgAoY62YLF1X5UiDzu"  # API_KEY dal mio account plantNet
PROJECT = "weurope"  #identifica la zona di interesse in cui fare la ricerca
api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"  #url a cui fare la richiesta
# data = {
#    'organs': ['leaf', 'leaf', 'leaf', 'leaf']}  #deve esere della stessa lunghezza della lista di immagini


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
        Non ho capito se è una lista di FileIO o BinaryIO
    '''
    files = []
    if len(photos) <= 5:
        for photo in photos:
            image_data = open(photo, 'rb')
            files.append(('images', (photo, image_data)))
    print(files)
    return files

def sendImg(files):
    data = {'organs': []}
    organ = 'leaf'
    for file in files:
        data['organs'].append(organ)
    req = requests.Request('POST',
                           url=api_endpoint,
                           files=files,
                           data=data)
    prepared = req.prepare()
    s = requests.Session()
    response = s.send(prepared)
    json_result = json.loads(response.text)
    try:
        specie = json_result['results'][0]['species']['scientificName']
        affidabilità = (json_result['results'][0]['score'])
        genus = json_result['results'][0]['species']['genus'][
            'scientificNameWithoutAuthor']
        family = json_result['results'][0]['species']['family'][
            'scientificNameWithoutAuthor']
        commonName = json_result['results'][0]['species']['commonNames'][0]

    except:
        specie = (json_result['bestMatch'])
        affidabilità = 'n.d.'
        genus = 'n.d.'
        family = 'n.d.'
        commonName = 'n.d.'
        identificazione = [specie]

    finally:
        identificazione = [specie, affidabilità, genus, family, commonName]
        return identificazione
