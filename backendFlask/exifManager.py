from pprint import pprint
from PIL import Image
import piexif

codec = 'ISO-8859-1'  # or latin-1, serve a decodificare i tag exif


class ExifManager:
    '''accetta un immagine e restituisce il dizionario con gli exif'''

    def img_opener(image):
        im = Image.open(image)
        exif_dict = piexif.load(im.info.get('exif'))
        return exif_dict

    '''accetta un dizionario di exif e restituisce solo i tag relativi al GPS
    estrae sololatitudine e longitudine'''

    def exif_to_tag(exif_dict):
        exif_tag_dict = {}
        thumbnail = exif_dict.pop('thumbnail')
        exif_tag_dict['thumbnail'] = thumbnail.decode(codec)

        for ifd in exif_dict:
            exif_tag_dict[ifd] = {}
            for tag in exif_dict[ifd]:
                try:
                    element = exif_dict[ifd][tag].decode(codec)

                except AttributeError:
                    element = exif_dict[ifd][tag]

                exif_tag_dict[ifd][piexif.TAGS[ifd][tag]["name"]] = element
        return 'lat', exif_tag_dict['GPS'][
            'GPSLatitude'], 'long', exif_tag_dict['GPS']['GPSLongitude']
