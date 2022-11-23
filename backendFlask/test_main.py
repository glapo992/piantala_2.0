from plantnet import PlantNet as pt
import json
from jpg_image_conversion import ConvertImg as ci

FILEPATH = '/Users/giuliolapovich/Code/aws-azure/piantala/backendFlask/static/src/identification.txt'
#---------FILE TEMPORANEO PER PROVARE API ------------
'''lista di 5 imamgini locali per vedere se la api funziona
la lista verrà compilata con le immagini fornite dal form
'''

image1 = '/Users/giuliolapovich/Code/aws-azure/piantala/backendFlask/static/img/piante/salvia.jpg'
image2 = '/Users/giuliolapovich/Code/aws-azure/piantala/backendFlask/static/img/piante/salvia1.jpg'
image3 = '/Users/giuliolapovich/Code/aws-azure/piantala/backendFlask/static/img/piante/salvia2.jpg'
image4 = '/Users/giuliolapovich/Code/aws-azure/piantala/backendFlask/static/img/piante/salvia3.jpg'

images_salvia = [image1, image2, image3, image4]

#prima di passare le immagini alla api le converto in jpg
files = pt.readImg(images_salvia)

result = pt.sendImg(files)

#teporaneo, salva il result su file txt per sviluppo. cancellare per prima del deploy
with open(FILEPATH, 'w') as outfile:
    json.dump(result, outfile)
