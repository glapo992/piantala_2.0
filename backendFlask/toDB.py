import uuid
# import json
import firebase_admin as firebase
from firebase_admin import credentials
from firebase_admin import firestore


class Firestore:
    '''
    Accetta due liste, una con la geolocalizzazione e una con la risposta di Plant.NET,
    genera un id unico e carica tutto in un nuovo documento su Firestore.
    '''

    def sendData(self, tagGPS, plantNET):
        # Costanti
        CRED = credentials.Certificate('../firebase-auth.json')
        APP = firebase.initialize_app(CRED)
        DB = firestore.client(APP)
        PIANTE_COLLECTION = DB.collection(u'piante')
        # Genera nuovo UUID
        unique_id = uuid.uuid1()
        # Aggiungi una nuova pianta a Firestore
        pianta = PIANTE_COLLECTION.document(unique_id)
        pianta.set({
                       u'nome comune': plantNET[4],
                       u'affidabilità': plantNET[1],
                       u'specie': plantNET[0],
                       u'genere': plantNET[2],
                       u'famiglia': plantNET[3],
                       u'lat': tagGPS[0],
                       u'long': tagGPS[1],
                   })
    '''
    Ritorna la lista completa di piante caricate sul database Firestore,
    in formato facilmente leggibile all'occhio umano
    '''

    def retrieveData(self):
        # Costanti
        CRED = credentials.Certificate('../firebase-auth.json')
        APP = firebase.initialize_app(CRED)
        DB = firestore.client(APP)
        PIANTE_COLLECTION = DB.collection(u'piante')
        # Scarica la lista dei dati e stampala
        piante = PIANTE_COLLECTION.stream()
        for pianta in piante:
            dati_pianta = pianta.to_dict()
            print(f'{dati_pianta["nome comune"]}, con affidabilità {dati_pianta["affidabilità"]}')
        #TODO: trasformare il dizionario in JSON invece di stamparlo a terminale
        

'''
tagGPS[0] = latitudine
tagGPS[1] = longitudine
risposta:
        0 = specie
        1 = affidabilità risposta
        2 = genere
        3 = famiglia
        4 = nome comune
'''
