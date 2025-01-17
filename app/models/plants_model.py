from app.models import db, datetime, Config
from .user_model import Users


""" useful query:
Plant_mini.query.delete()
Specie.query.delete()
Genus.query.delete()
Family.query.delete()

flask db stamp head
flask db migrate
flask db upgrade
"""


class Plant(db.Model):
    """ Table to use when I understand how to make the user to load 5 images and 5 organs"""
    id          = db.Column(db.Integer, primary_key = True)
    timestamp   = db.Column(db.DateTime, index = True, default=datetime.utcnow)
    # paths of the images saved in the filesystem
    img_1       = db.Column(db.String(100), nullable = False)
    img_2       = db.Column(db.String(100), nullable = True)
    img_3       = db.Column(db.String(100), nullable = True)
    img_4       = db.Column(db.String(100), nullable = True)
    img_5       = db.Column(db.String(100), nullable = True)
    # organs from the form
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

class Plant_mini(db.Model):
    """ Temp class for dev, must find a solution to fill the big one above with just one form that repeats itself and datas from API response"""
    id          = db.Column(db.Integer, primary_key = True)
    timestamp   = db.Column(db.DateTime, index = True, default=datetime.utcnow)
    img_1       = db.Column(db.String(100), nullable = False)
    organ_1     = db.Column(db.String(30), nullable = False)
    reliability = db.Column(db.Float())
    is_complete = db.Column(db.Boolean) # True if the response is complete
    specie_id   = db.Column(db.Integer, db.ForeignKey('specie.id'))
    lat         = db.Column(db.Float())
    long        = db.Column(db.Float())
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = True) 


    def create_plant(self, img_path:str, organ:str, result:list[str], tagGPS:list[str], user_id = user_id):
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
        self.lat        = tagGPS[0]
        self.long       = tagGPS[1]
        self.user_id    = user_id

        # check if the api returned full ans or partial only
        #print('result len:' , len(result))
        if len(result) > 5:
            self.reliability = result[1]
            self.is_complete = True  # store the status of the response, if complete or not
            self.specie_id   = Specie.add_specie(specie_name=result[0], common_name=result[4],genus_name=result[2],family_name=result[3])
            #print('models specie id:', self.specie_id)
        else:
            self.specie_id = Specie.add_specie(specie_name=result[0])
            self.is_complete = False

    
    def search_specie(self, page)->list:
        """ Search other pics in th DB of the same specie

        :return: list of picture paths 
        :rtype: list[Plant_mini]
        """

        plants_list = Plant_mini.query.filter_by(specie_id = self.specie_id).paginate(page=page, per_page=Config.IMG_PER_PAGE, error_out=False)
        #for plant in plants_list:
        #    path_list.append(plant.img_1)
        #print('path list ->', path_list)
        return plants_list
    
    def locate_specie(self)->dict:
        """ Build a dict of the coordiantes of all plants to display on the map and the specie name

        :return: dict lat, long, specie_name
        :rtype: dict
        """
        coo_dict = {}
        plants_list =  Plant_mini.query.filter_by(specie_id = self.specie_id).all() # search only plants of the same specie of the observed one
        specie = Specie.query.filter_by(id = self.specie_id).first()
        #plants_list =  Plant_mini.query.all() # search all plants on db
        for plant in plants_list:
            #print ('location func - plant_id: ', plant.id)
            tmp_dict = {}
            tmp_dict['lat']  = plant.lat if plant.lat else None
            tmp_dict['long'] = plant.long if plant.long else None
            tmp_dict['specie_name'] = specie.specie_name
            coo_dict[plant.id] = tmp_dict
            
        return coo_dict

class Specie(db.Model):
    id          = db.Column(db.Integer, primary_key = True) 
    specie_name = db.Column(db.String(50))
    common_name = db.Column(db.String(50))
    genus_id    = db.Column(db.Integer, db.ForeignKey('genus.id'))
    plants      = db.relationship('Plant_mini', backref = 'included', lazy = 'dynamic')

    @staticmethod
    def add_specie(specie_name:str, common_name :str = None, genus_name:str = None, family_name:str = None )-> int:
        """ Check if the specie already exists, else it creates one. To do that must check on cascade also genus and family.
        if there is a partial identification and later a full of the same specie, the record is updated with other datas

        :param specie_name: scientific name of the specie
        :type specie_name: str
        :param common_name: common name of the specie, defaults to None
        :type common_name: str, optional
        :param genus_name: name of the genus, defaults to None
        :type genus_name: str, optional
        :param family_name: name of the family, defaults to None
        :type family_name: str, optional
        :return: id of the Specie 
        :rtype: int
        """
        s = Specie.query.filter_by(specie_name = specie_name).first()
        print('specie -> s.common_name:',s.common_name) if s and s.common_name else print ('Specie not found')
        if s and s.common_name and s.genus_id: #if the record is complete just pass the ID of the specie
            print ('add_specie - if ->',s.common_name)
            return s.id
        elif s and not (s.common_name and s.genus_id):  # if the specie altready exist but the record is not complete, tries to add other info to the db
            s.common_name = common_name
            s.genus_id    = Genus.add_genus(genus_name, family_name)
            print ('add_specie - elif ->',s.common_name)
            try:
                #db.session.add(s)
                db.session.commit()
                return s.id
            except Exception('impossible to write on the database'):
                return s.id
        else:               # if the specie is not on the database, creates a new record
            if common_name: # if the api doest provide full identification there are no info to pass ahead
                genus_id = Genus.add_genus(genus_name, family_name)
                #print('models genus id:', genus_id)
                s = Specie(specie_name = specie_name, common_name = common_name, genus_id = genus_id)
            else:
                s = Specie(specie_name = specie_name)
            try:
                db.session.add(s)
                db.session.commit()
                print ('add_specie - else ->',s.id)
                return s.id
            except Exception('impossible to write on the database'):
                return s.id
                

class Genus(db.Model):
    id         = db.Column(db.Integer, primary_key = True) 
    genus_name = db.Column(db.String(50))
    family_id  = db.Column(db.Integer, db.ForeignKey('family.id'))
    species    = db.relationship('Specie', backref = 'included', lazy = 'dynamic')

    @staticmethod
    def add_genus(genus_name:str = None, family_name:str = None)->int:
        """ Check if the genus is already on the database, else creates new one. To do that must check on cascade also family

        :param genus_name: name of the genus
        :type genus_name: str
        :param family_name: name of the family
        :type family_name: str
        :return: id of the genus
        :rtype: int
        """
        g = Genus.query.filter_by(genus_name = genus_name).first()
        if g:
            return g.id
        else:
            family_id = Family.add_familiy(family_name = family_name)
            print('models family id:', family_id)
            g = Genus(genus_name = genus_name, family_id = family_id)
            try:
                db.session.add(g)
                db.session.commit()
                return g.id
            except Exception('impossible to write on the database'):
                return g.id

class Family(db.Model):
    id      = db.Column(db.Integer, primary_key = True) 
    family_name  = db.Column(db.String(50))
    genuses = db.relationship('Genus', backref = 'included', lazy = 'dynamic')

    @staticmethod
    def add_familiy(family_name:str = None)-> int:
        """ Check if the family already exists, else creates it

        :param family_name: name of the family 
        :type family_name: str
        :return: id of the family
        :rtype: int
        """
        print('models.family_name', family_name)
        f = Family.query.filter_by(family_name = family_name).first()
        if f:
            print('if f -> f.id: ', f.id)
            return f.id
        else:
            f = Family(family_name = family_name)
            print('else not f -> f.id', f.id)
            try:
                    db.session.add(f)
                    db.session.commit()
                    return f.id
            except Exception('impossible to write on the database'):
                    return f.id
            

