import os
from config import Config
from datetime import datetime


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
        os.remove(os.path.join(path, image))


'''def store_pics():
    """move all the content of the temp folder to a definitive one in fileserver"""
    root = os.path.join(basedir, 'fileserver')
    upload_folder = Config.UPLOAD_FOLDER
    folder_counter = 0
    # build folder name
    folder_name = datetime.strftime(datetime.now(), '%Y_%m_%d')+'_'+ str(folder_counter)
    dest_folder = os.path.join(root,folder_name)
    # add a numnber after the folder name 

    while os.path.isdir(dest_folder):
        folder_counter += 1
        folder_name = datetime.strftime(datetime.now(), '%Y_%m_%d')+'_'+ str(folder_counter)
        dest_folder = os.path.join(root,folder_name)    
    # copy upload folder in dest folder
    shutil.copytree(upload_folder, dest_folder)
    return dest_folder
'''