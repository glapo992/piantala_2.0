"""# conversione di ogni tipo di immagine in jpg per mandarlo a plantnet
from PIL import Image


def convertJpg(image):
    '''
    Accetta string con path dell' immagine salvata in upload
    converte immagine in jpg
    salva immagine su cartella static/tmp/conv/

    Parameters:
    ---
    image : str
        Path dell'immagine

    Returns:
    ---
    converted_image_path : str
        Percorso nuova immagine
    '''
    # Importa l'immagine
    im = Image.open(image)
    # Converte in jpg
    rgb_im = im.convert("RGB")
    # Cambia il path per l'esportazione
    imageconv = image.replace('upload', 'conv')
    # Esporta l'immagine
    rgb_im.save(imageconv + '_conv.jpg')
    converted_image_path = (imageconv + '_conv.jpg')
    return converted_image_path
"""