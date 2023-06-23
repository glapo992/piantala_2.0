from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import  SubmitField, FieldList, FormField, SelectField
from wtforms.validators import DataRequired, ValidationError
from werkzeug.utils import secure_filename
from utils.utils import allowed_file
from config import Config, basedir
from datetime import datetime
import shutil
import os


# https://stackoverflow.com/questions/30121763/how-to-use-a-wtforms-fieldlist-of-formfields
class ImageForm(FlaskForm):
    photo = FileField("image", validators=[DataRequired()])
    organ = SelectField(u'che parte di pianta sto guardando?',choices=[('foglia', 'leaf'), ('ramo', 'branch'), ('radice', 'root')] ) #TODO: add the correct choiches list
    submit= SubmitField ('invia')

    def upload(self, up_folder:str)->str: # TODO refacor and move logic somewhere else
        """ write the images from the form in the temp folder
        
        :return: path to the source
        :rtype:str
        """
        if self.photo.data and allowed_file(self.photo.data.filename):
            filename = secure_filename(self.photo.data.filename)
            self.photo.data.save(os.path.join(up_folder, filename))
        return filename

    def store_pics(self):
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


class ImageList(FlaskForm):
    images_list = FieldList(FormField(ImageForm), min_entries=1, max_entries=5)

