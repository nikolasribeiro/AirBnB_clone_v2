#!/usr/bin/python3
"""test for databasse storage"""
import unittest
from models.place import Place
from models.state import State
from models.city import City
from models.review import Review
from os import getenv
import MySQLdb
import pep8
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.engine.db_storage import DBStorage
from models import storage
import os
import MySQLdb


class TestDataBaseStorage(unittest.TestCase):
    """Test for the Database"""

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != 'db',
                     "Don´t run if is file storage")
    def setUp(self):
        """Run at the begining of each method"""
        if os.getenv("HBNB_TYPE_STORAGE") == 'db':
            self.db = MySQLdb.connect(os.getenv("HBNB_MYSQL_HOST"),
                                      os.getenv("HBNB_MYSQL_USER"),
                                      os.getenv("HBNB_MYSQL_PWD"),
                                      os.getenv("HBNB_MYSQL_DB"))
            self.cursor = self.db.cursor()

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != 'db',
                     "Don´t run if is file storage")
    def tearDown(self):
        """Run at the end of each method"""
        if os.getenv("HBNB_TYPE_STORAGE") == 'db':
            self.db.close()

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db',
                     "Don´t run if is file storage")
    def test_attributes_DBStorage(self):
        """Test the methods"""
        self.assertTrue(hasattr(DBStorage, 'new'))
        self.assertTrue(hasattr(DBStorage, 'save'))
        self.assertTrue(hasattr(DBStorage, 'all'))
        self.assertTrue(hasattr(DBStorage, 'delete'))
        self.assertTrue(hasattr(DBStorage, 'reload'))
        self.assertTrue(hasattr(DBStorage, '_DBStorage__engine'))
        self.assertTrue(hasattr(DBStorage, '_DBStorage__session'))

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db',
                     "Don´t run if is file storage")
    def test_pep8_DataBaseStorage(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

if __name__ == "__main__":
    unittest.main()