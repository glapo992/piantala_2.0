from app import db
from datetime import datetime


class Identification(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    timestamp   = db.Column(db.DateTime, index = True, default=datetime.utcnow)
    # paths of the images saved in the filesystem
    img_1       = db.Column(db.String(100), nullable = False)
    img_2       = db.Column(db.String(100), nullable = True)
    img_3       = db.Column(db.String(100), nullable = True)
    img_4       = db.Column(db.String(100), nullable = True)
    img_5       = db.Column(db.String(100), nullable = True)
    # organ from the form
    organ_1     = db.Column(db.String(30), nullable = False)
    organ_2     = db.Column(db.String(30), nullable = True)
    organ_3     = db.Column(db.String(30), nullable = True)
    organ_4     = db.Column(db.String(30), nullable = True)
    organ_5     = db.Column(db.String(30), nullable = True)
    reliability = db.Column(db.Float())
    specie      = db.Column(db.String(50))
    genus       = db.Column(db.String(50))
    family      = db.Column(db.String(50))
    commonName  = db.Column(db.String(50))
    lat         = db.Column(db.Float())
    long        = db.Column(db.Float())


class Identification_mini(db.Model):
    """temp class for dev, must find a solution to fill the big one above with just one form that repeats itself and datas from API response"""
    id          = db.Column(db.Integer, primary_key = True)
    timestamp   = db.Column(db.DateTime, index = True, default=datetime.utcnow)
    img_1       = db.Column(db.String(100), nullable = False)
    organ_1     = db.Column(db.String(30), nullable = False)
    reliability = db.Column(db.Float())
    specie      = db.Column(db.String(50))
    genus       = db.Column(db.String(50))
    family      = db.Column(db.String(50))
    commonName  = db.Column(db.String(50))
    lat         = db.Column(db.Float())
    long        = db.Column(db.Float())

    

"""
Identification_mini.query.delete
"""