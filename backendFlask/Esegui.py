from plantnet import PlantNet as pt
from exifManager import ExifManager as em


class esegui:

    def __init__(self, imagesList):
        self.imagesList = imagesList

    '''produce i dati da inviare al DB gia formattati'''

    def leggiGPS(imagesList):
        #apre la prima immagine della lista in binario
        openImg = em.img_opener(imagesList[0])
        #legge dati GPS
        gpsInfo = em.exif_to_tag(openImg)
        return gpsInfo

    def ottieniRisposta(imagesList):
        #pare le immagini in bianrio
        files = pt.readImg(imagesList)
        #invia immaigni alla api
        result = pt.sendImg(files)
        return result
