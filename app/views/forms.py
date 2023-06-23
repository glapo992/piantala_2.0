from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import  SubmitField, FieldList, FormField, SelectField
from wtforms.validators import DataRequired, ValidationError
from config import Config
from werkzeug.utils import secure_filename
from utils.utils import allowed_file

import os


# https://stackoverflow.com/questions/30121763/how-to-use-a-wtforms-fieldlist-of-formfields
class ImageForm(FlaskForm):
    photo = FileField("image", validators=[DataRequired()])
    organ = SelectField(u'che parte di pianta sto guardando?',choices=[('foglia', 'leaf'), ('ramo', 'branch'), ('radice', 'root')] ) #TODO: add the correct choiches list
    submit= SubmitField ('invia')

    def upload(self):
        """ write the images from the form in the specified folder """
        if self.photo.data and allowed_file(self.photo.data.filename):
            filename = secure_filename(self.photo.data.filename)
            self.photo.data.save(os.path.join(Config.UPLOAD_FOLDER, filename))


class ImageList(FlaskForm):
    images_list = FieldList(FormField(ImageForm), min_entries=1, max_entries=5)

