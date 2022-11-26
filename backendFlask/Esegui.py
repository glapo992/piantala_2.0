from plantnet import PlantNet as pt
from exifManager import ExifManager as em


class esegui:

    def __init__(self, imagesList):
        self.imagesList = imagesList

    '''produce i dati da inviare al DB gia formattati'''

    def leggiGPS(imagesList):
        openImg = em.img_opener(imagesList[0])
        gpsInfo = em.exif_to_tag(openImg)
        return gpsInfo

    def ottieniRisposta(imagesList):
        files = pt.readImg(imagesList)
        result = pt.sendImg(files)
        return result
