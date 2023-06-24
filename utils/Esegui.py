from utils.plantnet import readImg, sendImg
from  utils.exifManager import img_opener, exif_to_tag


def leggiGPS(imagesList):
    '''
    Ritorna una lista di coordinate GPS

    Parameters
    ---
    imagesList : list[str]
        Una lista di path di immagini

    Returns
    ---
    gpsInfo : list[float]
        Una lista con le coordinate GPS della prima immagine
    '''
    # Apre la prima immagine della lista in binario
    openImg = img_opener(imagesList[0])
    # Legge dati GPS
    gpsInfo = exif_to_tag(openImg)
    return gpsInfo

def ottieniRisposta(imagesList, organs_list):
    '''
    Ritorna la risposta di Plant.NET

    Parameters
    ---
    imagesList : list[str]
        Una lista di immagini

    Results
    ---
    result : list[str]
        Lista contenente i risultati dell'analisi
    '''
    # Apre le immagini in bianrio
    files = readImg(imagesList)
    # Invia immagini alla API
    result = sendImg(files, organs=organs_list)
    return result
