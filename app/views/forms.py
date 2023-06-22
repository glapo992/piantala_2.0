from flask_wtf import FlaskForm
from wtforms import  SubmitField,  FileField, FieldList, FormField, SelectField
from wtforms.validators import DataRequired, ValidationError
from config import Config

import os


# https://stackoverflow.com/questions/30121763/how-to-use-a-wtforms-fieldlist-of-formfields
class ImageForm(FlaskForm):
    photo = FileField("photo")
    organ = SelectField(u'che parte di pianta sto guardando?',choices=[('foglia', 'leaf'), ('ramo', 'branch'), ('radice', 'root')] ) #TODO: add the correct choiches list

class ImageList(FlaskForm):
    images_list = FieldList(FormField(ImageForm), min_entries=1, max_entries=5)
    submit      = SubmitField ('invia')

    def upload(request):
        """ write the images from the form in the specified folder """
        form = ImageList(request.POST)
        if form.image.data:
            image_data = request.FILES[form.image.name].read()
            open(os.path.join(Config.UPLOAD_FOLDER), 'w').write(image_data)




class EmtyForm(FlaskForm):
    """allows to generate a form with only a button, so you can integrate it as a POST request and send data without make them appear in the url like a GET"""
    submit = SubmitField('Submit')