import os
from config import Config


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
    """ Check that the input file has an allwed extension 

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
        os.remove(path + image)
