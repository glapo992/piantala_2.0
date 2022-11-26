from flask import Flask, render_template, request, url_for, redirect
from plantnet import *
from Esegui import esegui
from dataviz import Dataviz as dv

app = Flask(__name__)
'''il render_template apre il file all'interno della cartella templates'''


@app.route('/')
def index():
    return render_template('index.html')


'''pagina vuota dimostrativa'''


@app.route('/progetto1')
def progetto1():
    return render_template('progetto1.html')


'''ogni volta che viene chiamato il metodo per generare la mappa, questo file html viene sovrscritto con i dati nuovi'''


@app.route('/circle_map')
def circle_map():
    return render_template('circle_map.html')


@app.route('/about')
def about():
    image1 = 'static/img/piante/img1.JPG'
    image2 = 'static/img/piante/img2.JPG'
    image3 = 'static/img/piante/img3.JPG'
    image4 = 'static/img/piante/img4.JPG'
    imagesList = [image1, image2, image3, image4]
    '''accetta lista immagini, restituisce lista di 2 elementi gps lat e lon'''
    tagGPS = esegui.leggiGPS(imagesList=imagesList)
    '''accetta lista immaigni e restituisce un json con risposte api'''
    #risposta = esegui.ottieniRisposta(imagesList=imagesList)
    '''accetta lista con lat e lon e restituisce oggetto html'''
    map = dv.mappa_provv(tagGPS)

    #return render_template('about.html', risposta=risposta, tagGPS=tagGPS)
    return render_template('about.html', tagGPS=tagGPS)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# #--------------------------test form------------------
# import os
# from flask import Flask, flash, request, redirect, url_for
# from werkzeug.utils import secure_filename

# UPLOAD_FOLDER = '/Piantala/backendFLask/tmp/uploads'
# ALLOWED_EXTENSIONS = {'raw', 'png', 'jpg', 'jpeg', 'gif'}

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('download_file', name=filename))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''
#-----------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)