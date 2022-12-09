import firebase_admin as firebase
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import json


EMERGENCY_JSON = '''{
  "type": "service_account",
  "project_id": "piantala",
  "private_key_id": "7f4ece84631d54fdc8946bbefd0adb1d1bf249dc",
  "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQD6avCBf1e+ro1Z\\njXpQ6LqLrPelVljq25/+Yj+ihxl/V6eiBAxBQiyv/pgkx6282e9D5sY3VHDf+P85\\nhuMOfUsizb/oa1Ndu3v2nSH6LAVIhauzQk3hpyWa2UE5X2F0th72Cdm7hAtd5w6z\\nSMsrBZBt/4YoI16cjavYiqqWVQNkfAnwfeuPRwq3iHr7Ft6bVrQLxRXAVogOJeSW\\nkLvz+/q6x00ETJW8duOuodrK1ihvy5hbMb+pqvewbn3h+MCdvKltc18Al+4nBG3v\\nWjVVdgTvSBTzjVu0SZxwvaUOebcrMq2uT6Ag+kMdd1R+sPX6ANNHdmZQi6DBZIKu\\nhYzq1L+BAgMBAAECggEARtvYx0Px376Dt8ntSRS5qIlen/XRfk98M964M/S3lc2H\\nXTR5BURE4d4QTiQEePJQHm4gO4rUz8Ok8LHG8RQqHSSMP6eS9Ox21N88vI4VRqKw\\nZa6G3CnQXcNJDgN7z6szEprR9hoUn1Mg2UFpX/iYmE+cNiJgBLuf20vNnnFa3uUd\\nHLV0Fs+CISJEYaUzxhNcYd4X1VrASJYnInOIsDwoakKlGfm84jllC55O5yUHzDn7\\nCOJIKRu8pep3laElv/Lt0m1krj+gfEGqLXoK0YM9QEj+zIlo4368zhuBK5Tu8OIg\\nutYGTLHoy6Panjm8VYSCrmvsmg0igvdNONb5W1HpQwKBgQD/tNfgI3zmmFveDwEX\\n2/oUBy5LWZ6LGXnsJYa5kWm/mpkTTlCz0NdNlRV4NCM9/gvaHx6smlu+RaYDsLYn\\ny9mCE89xaD5PgqsY5K9l+8tQnCqtwR2yrUQ1thSUGwoXz7p86Ax6s3svW+WXu2wB\\n6EHH56wX5Br3wgUgjB8wf22HPwKBgQD6tIqxitd/dw5VEf+SngykQLcnHutt3bct\\nQbNgXP8LPRKlS605xEa+Lm4OWLeOESzC9vGFjM8NODADFbBoVjA977+6qTVL5gzO\\nn79QCw435XKMhjhzHWA+1Djp3mrDUGIoIh1jf0mlf3MvI9PvHerNZ/fR5HDDR7mp\\nvK9CtFDJPwKBgCLlm1CLh1AxGtiDU7Ld4pM5J6hA4tI499qyhGBu5++uOZXY6kqg\\nBcIgxn1RID4lnZh3BsiniD2/Y5i9VR65Q0XtTjI798UCIDeVfhp88pJdvbVY1aS8\\n4MIzxzsvNYFqaBkD0jAsrnMYJ409ls/r0o5ln6bjCoslf22hsd/8hAYhAoGAL4u/\\n5e3r8quUl0OjkZ3RzfDMC2pMwfhTfgzAxRy97da2S4zvnE4CEJ1jl+rxXMsbDxqg\\nMXDD78DhMiSR4Se/XG+0j+T5S5ykfydCtB50otsr/0SRPhurHh9Hb+sTmlkLVIsr\\nwavpPq7OHHmR/v5QgoYeNLs7O33F01AKeP8TdycCgYEAoa7gTGDTU8eleeZocSRs\\nMxdzeNZxH+McvSO00o2b0JaUXrbAQ32b53V+efyNTfVyBuu5Ivjk4V+v4aMmbRll\\nxt8A9a/+bsu0ey/c0fS7IBQZ0d79Wx66Tf4AGOXReQUbsn9dnDnRxuGS21S0N6BZ\\niIU9aiJBEE8hHunp36fC8zA=\\n-----END PRIVATE KEY-----\\n",
  "client_email": "firebase-adminsdk-t7mh1@piantala.iam.gserviceaccount.com",
  "client_id": "102443266997900877757",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-t7mh1%40piantala.iam.gserviceaccount.com"
}'''

try:
    CRED = credentials.Certificate('firebase-auth.json')
except:
    with open('firebase-auth.json', 'w') as auth:
       auth.write(EMERGENCY_JSON)
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
