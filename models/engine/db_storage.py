#!/usr/bin/python3
"""This is the database storage class for AirBnB"""
import os

from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session


class DBStorage:
    """This class serializes instances to a JSON file and
    deserializes JSON file to instances
    Attributes:
        __file_path: path to the JSON file
        __objects: objects will be stored
    """
    __engine = None
    __session = None

    def __init__(self):
        user = os.getenv("HBNB_MYSQL_USER")
        pwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")
        env = os.getenv("HBNB_ENV")
        engine_str = "mysql+mysqldb://{}:{}@{}/{}".format(user, pwd, host, db)
        self.__engine = create_engine(engine_str, pool_pre_ping=True)
        Base.metadata.bind = self.__engine
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        my_dict = {}

        if cls:
            for obj in self.__session.query(eval(cls)).all():
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                my_dict[key] = obj
        else:
            for subcls in classes:
                for obj in self.__session.query(subcls).all():
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    my_dict[key] = obj

        return my_dict

    def new(self, obj):
        """ Set in obj as a database entry """
        self.__session.add(obj)

    def save(self):
        """ commit saves to database """
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ removes a private session attribute """
        self.__session.close()
