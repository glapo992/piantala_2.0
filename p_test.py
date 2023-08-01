import os
from datetime import datetime, timedelta
import string 
import random
import unittest
from app import create_app, db
from app.plantnet import plantnet
from app.models import Plant_mini, Family, Genus, Specie
from config import Config
from app.static.src.identification_sample import IDENT_FULL, IDENT_PART

basedir = os.path.abspath(os.path.dirname(__file__))
class TestConfig(Config):
    TTESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    UPLOAD_FOLDER = '.'
    CONVERTED_FOLDER = '.'
    JSON_FOLDER = '.'

class PlantInsertionCase(unittest.TestCase):

    def setUp(self) -> None:
        """set the context of the test, executed the beginning, the context stays in memory and is not saved"""
        self.app = create_app(TestConfig)
        print(TestConfig.SQLALCHEMY_DATABASE_URI)
        self.app_context = self.app.app_context()  # create a new application context
        self.app_context.push()
        db.create_all()   # creates all db tables
        
    
    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_result_list_full(self):
        result = plantnet.plant_json_to_list(json_result=IDENT_FULL)
        self.assertEqual(result[0],  "Salvia officinalis" )
        self.assertIsInstance(result[1], float)
        self.assertEqual(result[1],  IDENT_FULL['results'][0]['score'])
        self.assertIsInstance(result[2], str)
        self.assertEqual(result[2],  "Salvia" )
        self.assertIsInstance(result[3], str)
        self.assertEqual(result[3],  "Lamiaceae" )
        self.assertIsInstance(result[4], str)
        self.assertEqual(result[4],  "Sage" )
        self.assertIsInstance(result[5], int)

    def test_result_list_part(self):
        result = plantnet.plant_json_to_list(json_result=IDENT_PART)
        self.assertIsInstance(result[0],str)
        self.assertEqual(result[0],  IDENT_PART['bestMatch'].split('(')[0].strip() )
        self.assertIsInstance(result[1], int)

    def test_insert_plant_full(self):
        img_path = "path/to/file"
        organ    = "leaf"
        result   = [''.join(random.choices(string.ascii_uppercase +
                    string.digits, k= random.randint(0, 50))),
                    random.random(), 
                    ''.join(random.choices(string.ascii_uppercase +
                    string.digits, k= random.randint(0, 50))), 
                    ''.join(random.choices(string.ascii_uppercase +
                    string.digits, k= random.randint(0, 50))),
                    ''.join(random.choices(string.ascii_uppercase +
                    string.digits, k= random.randint(0, 50))),
                    random.randint(0, 500)]
        
        tagGPS   = [0,0]
        i = Plant_mini()
        i.create_plant(img_path, organ, result, tagGPS)
        db.session.add(i)
        db.session.commit()
        self.assertTrue(i.is_complete)
        self.assertEqual(i.organ_1, organ)
        self.assertEqual(i.specie_id, 1)
        s = Specie.query.filter_by(specie_name = result[0]).first()
        self.assertTrue(s.common_name)
        self.assertEqual(s.common_name, result[4] )
        self.assertEqual(s.genus_id, 1)
        g = Genus.query.filter_by(genus_name = result[2]).first()
        self.assertTrue(g.id, 1)
        self.assertEqual(g.genus_name, result[2] )
        self.assertEqual(g.family_id, 1)

    def test_insert_plant_part(self):
        img_path = "path/to/file"
        organ    = "leaf"
        result   = ["specie", 200]
        tagGPS   = [0,0]
        i = Plant_mini()
        i.create_plant(img_path, organ, result, tagGPS)
        self.assertFalse(i.is_complete)
        self.assertEqual(i.organ_1, 'leaf')
        self.assertEqual(i.specie_id, 1)
        s = Specie.query.filter_by(specie_name = result[0]).first()
        self.assertFalse(s.common_name)
        self.assertEqual(s.genus_id, None)

    def test_complete_data(self):
        #creating partial record
        img_path = "path/to/file"
        organ    = "leaf"
        specie_name = ''.join(random.choices(string.ascii_uppercase +
                    string.digits, k= random.randint(0, 50)))
        result_p = [specie_name,
                    random.randint(0, 500)]
        tagGPS   = [0,0]
        i_part = Plant_mini()
        i_part.create_plant(img_path, organ, result_p, tagGPS)
        db.session.add(i_part)
        db.session.commit()
        self.assertFalse(i_part.is_complete)
        s_part = Specie.query.filter_by(specie_name = result_p[0]).first()
        self.assertFalse(s_part.common_name)
        self.assertFalse(s_part.genus_id)

        # create complete record with same specie name
        result_c = [ specie_name,
                    random.random(), 
                    ''.join(random.choices(string.ascii_uppercase +
                    string.digits, k= random.randint(0, 50))), 
                    ''.join(random.choices(string.ascii_uppercase +
                    string.digits, k= random.randint(0, 50))),
                    ''.join(random.choices(string.ascii_uppercase +
                    string.digits, k= random.randint(0, 50))),
                    random.randint(0, 500)]
        i_compl = Plant_mini()
        i_compl.create_plant(img_path, organ, result_c, tagGPS) 
        db.session.add(i_compl)
        db.session.commit()
        self.assertTrue(i_compl.is_complete)
        self.assertNotEqual(i_part.id, i_compl.id)
        s_compl = Specie.query.filter_by(specie_name = result_p[0]).first()
        self.assertTrue(s_compl.common_name)
        self.assertTrue(s_compl.genus_id)
        # ensure that the part identificaton is completed by full info
        self.assertEqual(s_compl.id,s_part.id)
        self.assertEqual(s_compl.specie_name,s_part.specie_name)

if __name__ == '__main__':
    unittest.main(verbosity=3)