# conversione di ogni tipo di immagine in jpg per mandarlo a plantnet

from PIL import Image
import os

#image = '/Users/giuliolapovich/Code/aws-azure/piantala/backendFlask/static/tmp/upload/IMG_2074.JPG'


def convertJpg(image):
    '''accetta string con path dell' immagine salvata in upload
    converte immagine in jpg
    salva immagine su cartella static/tmp/conv/
    return: percorso nuova immagine'''
    # importing the image
    im = Image.open(image)
    # converting to jpg
    rgb_im = im.convert("RGB")
    # change path for exporting
    imageconv = image.replace('upload', 'conv')
    # exporting the image
    rgb_im.save(imageconv + '_conv.jpg')
    converted_image_path = (imageconv + '_conv.jpg')
    return converted_image_path


#convertJpg(image=image)
