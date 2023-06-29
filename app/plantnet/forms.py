from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import  SubmitField, SelectField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from utils.utils import allowed_file
from config import Config, basedir
from datetime import datetime
import shutil
import os

# https://stackoverflow.com/questions/30121763/how-to-use-a-wtforms-fieldlist-of-formfields
class ImageForm(FlaskForm):
    photo = FileField("image", validators=[DataRequired()])
    organ = SelectField(u'che parte di pianta è?',choices=[('auto', 'automatico'), ('leaf', 'foglia'), ('flower', 'fiore'), ('fruit', 'frutto'),('bark', 'corteccia')] )
    submit= SubmitField ('invia')

    def upload(self, up_folder:str)->str:
        """ Write the images from the form in the temp folder
        
        :return: path to the source
        :rtype:str
        """
        if self.photo.data and allowed_file(self.photo.data.filename):
            filename = secure_filename(self.photo.data.filename)
            self.photo.data.save(os.path.join(up_folder, filename))
            return filename

    def store_pics(self): # TODO refactor somewhere else
        """ Move all the content of the temp folder to a definitive one in fileserver
        for the moment in app/static/fileserver --> to move in an external source (apache webserver?)
        by now every picture has a folder --> for when more than one picture are accepted in the form"""
        root = os.path.join(basedir, 'app/static/fileserver') # the root of the fileserver
        upload_folder = Config.UPLOAD_FOLDER
        # build folder name
        folder_counter = 0
        folder_name = datetime.strftime(datetime.now(), '%Y_%m_%d')+'_'+ str(folder_counter)
        dest_folder = os.path.join(root,folder_name)
        # check if the folder name already exists and increase the counter
        while os.path.isdir(dest_folder): 
            folder_counter += 1
            folder_name = datetime.strftime(datetime.now(), '%Y_%m_%d')+'_'+ str(folder_counter)
            dest_folder = os.path.join(root,folder_name)    
        #print('dest folder:', dest_folder)
        
        shutil.copytree(upload_folder, dest_folder)     # copy upload folder in dest folder
        final_path = os.path.join('fileserver', folder_name) 
        print('path saved on DB without filename:', final_path)
        return final_path
   

# src="/static/fileserver/2023_06_29_0/bar3.jpg"