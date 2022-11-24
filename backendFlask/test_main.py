from plantnet import PlantNet as pt
from exifManager import ExifManager as em

#---------FILE TEMPORANEO PER PROVARE API ------------
'''lista di 5 imamgini locali per vedere se la api funziona
la lista verrà compilata con le immagini fornite dal form html
'''
image1 = '/Users/giuliolapovich/Code/aws-azure/piantala/backendFlask/static/img/piante/img1.jpg'
image2 = '/Users/giuliolapovich/Code/aws-azure/piantala/backendFlask/static/img/piante/img2.jpg'
image3 = '/Users/giuliolapovich/Code/aws-azure/piantala/backendFlask/static/img/piante/img3.jpg'
image4 = '/Users/giuliolapovich/Code/aws-azure/piantala/backendFlask/static/img/piante/img4.jpg'

imagesList = [image1, image2, image3, image4]

#lettura metadati GPS
openImg = em.img_opener(imagesList[0])
gpsInfo = em.exif_to_tag(openImg)

#prima di passare le immagini alla api vanno convertite in jpg

#invio ed identificazione immagini
files = pt.readImg(imagesList)
result = pt.sendImg(files)

print(result)
print(gpsInfo)
'''
#teporaneo, salva il result su file txt per SVILUPPO. cancellare per prima del deploy
with open('/Users/giuliolapovich/Code/aws-azure/piantala/backendFlask/static/src/identification.txt', 'w') as outfile:
     json.dump(result, outfile)

with open(
        '/Users/giuliolapovich/Code/aws-azure/piantala/backendFlask/static/src/gpsSample.txt',
        'w') as convert_file:
    convert_file.write(json.dumps(gpsInfo))
'''