from PIL import Image
import piexif

codec = 'ISO-8859-1'  # or latin-1, serve a decodificare i tag exif


class ExifManager:
    '''converte le coordinate da radaili (come escono dai tagGPS)a decimali (come le vuole folium'''

    def gpsConverter(cooDeg):
        cooDecimali = cooDeg[0] + ((cooDeg[1] + (cooDeg[2] / 60)) / 60)
        return cooDecimali

    '''accetta un immagine e restituisce il dizionario con gli exif
    --> da NON inviare al DB'''

    def img_opener(image):
        im = Image.open(image)
        exif_dict = piexif.load(im.info.get('exif'))
        return exif_dict

    '''accetta un dizionario di exif e restituisce solo i tag relativi al GPS in formato decimale
    estrae sololatitudine e longitudine
    --> da inviare al DB'''

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
        latDeg = [
            (exif_tag_dict['GPS']['GPSLatitude'][0][0]),
            (exif_tag_dict['GPS']['GPSLatitude'][1][0]),
            (exif_tag_dict['GPS']['GPSLatitude'][2][0] / 100),
        ]
        lonDeg = [
            (exif_tag_dict['GPS']['GPSLongitude'][0][0]),
            (exif_tag_dict['GPS']['GPSLongitude'][1][0]),
            (exif_tag_dict['GPS']['GPSLongitude'][2][0] / 100),
        ]
        print(latDeg)
        print(lonDeg)
        print(ExifManager.gpsConverter(latDeg), )
        print(ExifManager.gpsConverter(lonDeg))
        return [
            ExifManager.gpsConverter(latDeg),
            ExifManager.gpsConverter(lonDeg)
        ]
