# conversione di ogni tipo di immagine in jpg per mandarlo a plantnet
from PIL import Image
import os

def convertJpg(image_path:str, dest_folder:str)->str:
    """ convert any format of images into jpg, saves them in dest_folder and return its location

    :param image_path: path to the source
    :type image_path: str
    :param dest_folder: path to folder where to save the image
    :type dest_folder: str
    :return: path to the source
    :rtype:str
    """ 
    # Importa l'immagine
    im = Image.open(image_path)
    # Converte in jpg
    rgb_im = im.convert("RGB")
    filename = image_path.split('/')[-1] # name of the image
    print('filename: ', filename)
    converted_image_path = os.path.join(dest_folder, filename) + '_conv.jpg'
    print('conv img path: ', converted_image_path)
    rgb_im.save(converted_image_path)

    return converted_image_path
