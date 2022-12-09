import firebase_admin as firebase
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import json
import os


try:
    CRED = credentials.Certificate('firebase-auth.json')
except:
    firebase_json = {
        'type': os.environ.get('type'),
        'project_id': os.environ.get('project_id'), 
        'private_key_id': os.environ.get('private_key_id'), 
        'private_key': os.environ.get('private_key'), 
        'client_email': os.environ.get('client_email'), 
        'client_id': os.environ.get('client_id'), 
        'auth_uri': os.environ.get('auth_uri'), 
        'token_uri': os.environ.get('token_uri'), 
        'auth_provider_x509_cert_url': os.environ.get('auth_provider_x509_cert_url'), 
        'client_x509_cert_url': os.environ.get('client_x509_cert_url'), 
    }

    with open('firebase-auth.json', 'w') as auth:
        json.dump(firebase_json, auth)
    CRED = credentials.Certificate('firebase-auth.json')

APP = firebase.initialize_app(CRED)
DB = firestore.client(APP)
PIANTE_COLLECTION = DB.collection(u'piante')

def sendCompleteData(tagGPS, risposta):
    '''
    Carica i dati di un'identificazione completa su Firestore.

    Parameters
    ---
    tagGPS : list
        tag GPS da caricare
    plantNET : list
        risultati di plantNET da caricare
    '''
    # Genera nuovo UUID
    now = datetime.now()
    unique_id = datetime.strftime(now, '%y%m%d-%H%M%S-%f')
    # Aggiungi una nuova pianta a Firestore
    pianta = PIANTE_COLLECTION.document(unique_id)
    pianta.set({
                   u'nome comune': risposta[4],
                   u'affidabilità': risposta[1],
                   u'specie': risposta[0],
                   u'genere': risposta[2],
                   u'famiglia': risposta[3],
                   u'lat': tagGPS[0],
                   u'long': tagGPS[1],
               })


def sendPartialData(tagGPS, risposta):
    '''
    Carica i dati di un'identificazione parziale su Firestore.

    Parameters
    ---
    tagGPS : list
        tag GPS da caricare
    plantNET : list
        risultati di plantNET da caricare
    '''
    if risposta[0] != 'N/D':
        # Genera nuovo UUID
        now = datetime.now()
        unique_id = datetime.strftime(now, '%y%m%d-%H%M%S-%f')
        # Aggiungi una nuova pianta a Firestore
        pianta = PIANTE_COLLECTION.document(unique_id)
        pianta.set({
                       u'specie': risposta[0],
                       u'status': u'PARTIAL',
                       u'lat': tagGPS[0],
                       u'long': tagGPS[1],
                   })


def retrieveData(path):
    '''
    Crea un file .json in static/tmp/map con un array JSON con tutti i documenti del database e i relativi campi.
    Non ritorna e non richiede niente, è una funzione forte e indipendente del ventunesimo secolo.
    '''
    # Scarica la lista dei dati e stampala
    piante = PIANTE_COLLECTION.stream()
    piante_array = []
    for pianta in piante:
        # Trasforma il singolo record in dizionario
        pianta_dict = pianta.to_dict()
        # Aggiunge il JSON all'array
        piante_array.append(pianta_dict)
    # Scrive l'array in un file JSON
    with open(path + 'data.json', 'w') as file:
        json.dump(piante_array, file)


# Struttura liste passate
# tagGPS[0] = latitudine
# tagGPS[1] = longitudine
# risposta:
#         0 = specie
#         1 = affidabilità risposta
#         2 = genere
#         3 = famiglia
#         4 = nome comune
