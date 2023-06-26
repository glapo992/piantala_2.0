from app import db
from datetime import datetime


class Identification(db.Model):
    """table to use when I understand how to make the user to load 5 images and 5 organs"""
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
    """ temp class for dev, must find a solution to fill the big one above with just one form that repeats itself and datas from API response"""
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

    

    def create_plant(self, img_path:str, organ:str, result:list[str], tagGPS:list[str]):
        """ Assigns value from the result of an observation on the database colums

        :param img_path: path of the image in the fileserver
        :type img_path: str
        :param organ: organ related to the image 
        :type organ: str
        :param result: list elaborated form the response
        :type result: list[str]
        :param tagGPS: gps tags from images exif
        :type tagGPS: list[str]
        """     
        self.img_1      = img_path # path to the image
        self.organ_1    = organ

        # check if the api returned full ans or partial only
        if len(result) == 6:
            self.specie     = result[0]
            self.reliability= result[1]
            self.genus      = result[2]
            self.family     = result[3]
            self.commonName = result[4]
        else:
            self.specie = result[0]
        self.lat        = tagGPS[0]
        self.long       = tagGPS[1]

"""
Identification_mini.query.delete()
"""


