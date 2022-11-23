#src del codice: https://github.com/python-pillow/Pillow/issues/6199

from PIL import Image, TiffImagePlugin
import PIL.ExifTags
from pprint import pprint
import json

IMAGE_PATH = '/Users/giuliolapovich/Code/aws-azure/piantala/img/IMG_1980.jpg'


class ExifOpener:

    def readExif(photo):
        img = Image.open(photo)
        dct = {}
        for k, v in img._getexif().items():
            if k in PIL.ExifTags.TAGS:
                if isinstance(v, TiffImagePlugin.IFDRational):
                    v = float(v)
                elif isinstance(v, tuple):
                    v = tuple(
                        float(t) if isinstance(t, TiffImagePlugin.IFDRational
                                               ) else t for t in v)
                elif isinstance(v, bytes):
                    v = v.decode(errors="replace")
                dct[PIL.ExifTags.TAGS[k]] = v

        pprint(dct)
        pprint(
            '--------------------------------------------------------------------------------------------'
        )


pprint(dct['GPSInfo'])
outs = json.dumps(dct['GPSInfo'])

#Satampa il valore del dizionario corrispondente al GPSInfo ma non lo serializza in Json dando questo errore:

#TypeError: Object of type IFDRational is not JSON serializable

#devo vearamente crare un json a mano solo con i dati che miservono????
