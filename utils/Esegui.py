"""import plantnet as pt
import exifManager as em


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
    openImg = em.img_opener(imagesList[0])
    # Legge dati GPS
    gpsInfo = em.exif_to_tag(openImg)
    return gpsInfo

def ottieniRisposta(imagesList):
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
    files = pt.readImg(imagesList)
    # Invia immagini alla API
    result = pt.sendImg(files)
    return result
"""