from PIL import Image
import piexif
from config import Config



def gpsConverter(cooDeg:list)->list[float]:
    """ Converts coordinates from rad to decimal

    :param cooDeg: rad coordinates
    :type cooDeg: list[]
    :return: decimal coordinates
    :rtype: list []
    """
    cooDecimali = cooDeg[0] + ((cooDeg[1] + (cooDeg[2] / 60)) / 60)
    print('Coo dec type-> ', type(cooDecimali))
    return cooDecimali


def img_opener(image_path:str)->dict:
    """ Extract EXIF file from an image

    :param image_path: path oh the image
    :type image_path: str
    :return: dict with exif
    :rtype: dict
    """
    im = Image.open(image_path)
    exif_dict = piexif.load(im.info.get('exif'))
    return exif_dict


def exif_to_tag(exif_dict:dict)->list[float]:
    """ Extract lat e lon from the dict with EXIF

    :param exif_dict: dict with exif datas
    :type exif_dict: dict
    :return: gps coo in decimal format
    :rtype: list[float]
    """
    exif_tag_dict = {}
    thumbnail = exif_dict.pop('thumbnail')
    exif_tag_dict['thumbnail'] = thumbnail.decode(Config.CODEC)

    for ifd in exif_dict:
        exif_tag_dict[ifd] = {}
        for tag in exif_dict[ifd]:
            try:
                element = exif_dict[ifd][tag].decode(Config.CODEC)

            except AttributeError:
                element = exif_dict[ifd][tag]

            exif_tag_dict[ifd][piexif.TAGS[ifd][tag]["name"]] = element

    lat = [
        exif_tag_dict['GPS']['GPSLatitude'][0][0],
        exif_tag_dict['GPS']['GPSLatitude'][1][0],
        (exif_tag_dict['GPS']['GPSLatitude'][2][0] / 100)
    ]

    lon = [
        exif_tag_dict['GPS']['GPSLongitude'][0][0],
        exif_tag_dict['GPS']['GPSLongitude'][1][0],
        (exif_tag_dict['GPS']['GPSLongitude'][2][0] / 100)
    ]
    cooDec = [gpsConverter(lat), gpsConverter(lon)]

    return cooDec