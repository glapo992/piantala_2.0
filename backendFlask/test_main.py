from plantnet import PlantNet as pt

#---------FILE TEMPORANEO PER PROVARE API ------------
#lista di 5 imamgini locali per vedere se la api funziona
#la lista verrà compilata con le immagini fornite dal form

image1 = '/Users/giuliolapovich/Code/aws-azure/piantala/backendFlask/static/img/piante/salvia.jpg'
image2 = '/Users/giuliolapovich/Code/aws-azure/piantala/backendFlask/static/img/piante/salvia1.jpg'
image3 = '/Users/giuliolapovich/Code/aws-azure/piantala/backendFlask/static/img/piante/salvia2.jpg'
image4 = '/Users/giuliolapovich/Code/aws-azure/piantala/backendFlask/static/img/piante/salvia3.jpg'

images_salvia = [image1, image2, image3, image4]

files = pt.readImg(images_salvia)

result = pt.sendImg(files)

print(result)