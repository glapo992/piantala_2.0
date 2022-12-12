from PIL import Image
import piexif

codec = 'ISO-8859-1'  # or latin-1, serve a decodificare i tag exif


def gpsConverter(cooDeg):
    '''
    Converte le coordinate da radiali (come escono dai tagGPS) a decimali (come le vuole folium)

    Parameters
    ---
    cooDeg : list
        Litsa di coordinate radiali

    Returns
    ---
    cooDecimali : list
    '''
    cooDecimali = cooDeg[0] + ((cooDeg[1] + (cooDeg[2] / 60)) / 60)
    return cooDecimali


def img_opener(image):
    '''
    Estrae i dati EXIF da un'immagine.
    NB: i dati non sono pronti per essere inviati al database.

    Parameters
    ---
    image : string
        Il path di un'immagine

    Returns
    ---
    exif_dict : dict
        Un dizionario contenente i dati EXIF dell'immagine
    '''
    im = Image.open(image)
    exif_dict = piexif.load(im.info.get('exif'))
    return exif_dict


def exif_to_tag(exif_dict):
    '''
    Estrae da un dizionario di dati EXIF latitudine e longitudine

    Parameters
    ---
    exif_dict : dict
        Dizionario contenente i dati EXIF da parsare

    Returns
    ---
    cooDec : list[float]
        Coordinate GPS in formato radiale
    '''
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
