import os
from config import Config
from PIL import Image
import piexif


def generate_temp_folders()->None:
    """ generate folders where store temporary files
    * UPLOAD_FOLDER='static/tmp/upload'
    * CONVERTED_FOLDER='static/tmp/conv'
    * JSON_FOLDER='static/tmp/map'

    """
    temp_folders = [ Config.UPLOAD_FOLDER, Config.CONVERTED_FOLDER, Config.JSON_FOLDER ]
    for folder in temp_folders:
        if not os.path.exists(folder):
            os.makedirs(folder)


def allowed_file(filename:str)->bool:
    """ Check if the input file has an allwed extension 

    :param filename: input file name
    :type filename: str
    :return: true allowed
    :rtype: bool
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def clearfolder(path:str)->None:
    """ Deletes content of the folder in path

    :param path: path of the folder
    :type path: str
    """
    tmplist = os.listdir(path)
    for image in tmplist:
        os.remove(os.path.join(path, image))


def readImg(photos:list[str])->list:
    """ Reads a list of pics path, extract binary and retun all info in a list

    :param photos: List of pics path
    :type photos: list[str]
    :return: list of BinaryIO
    :rtype: list[str]
    """
    files = []
    if len(photos) <= 5:
        for photo in photos:
            image_data = open(photo, 'rb')
            files.append(('images', (photo, image_data)))
    return files  


def convertJpg(image_path:str, dest_folder:str)->str:
    """ convert any format of images into jpg, saves them in dest_folder and return its location

    :param image_path: path to the source
    :type image_path: str
    :param dest_folder: path to folder where to save the image
    :type dest_folder: str
    :return: path to the source
    :rtype:str
    """ 
    # Import of the Image
    im = Image.open(image_path)
    # Conversion to JPG
    rgb_im = im.convert("RGB")
    filename = image_path.split('/')[-1] # name of the image
    print('filename: ', filename)
    converted_image_path = os.path.join(dest_folder, filename) + '_conv.jpg'
    print('conv img path: ', converted_image_path)
    rgb_im.save(converted_image_path)

    return converted_image_path


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


def exif_reader(image_path:str)->dict:
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