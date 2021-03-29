#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime

Base = declarative_base()

class BaseModel:
    """A base class for all hbnb models"""
    
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if kwargs:
            self.__set_attributes(kwargs)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()


    def __set_attributes(self, attr_dict):
        """ __set_attributes method """

        if 'id' not in attr_dict:
            attr_dict['id'] = str(uuid4())

        if 'created_at' not in attr_dict:
            attr_dict['created_at'] = datetime.now()

        elif not isinstance(attr_dict['created_at'], datetime):
            attr_dict['created_at'] = datetime.strptime(
                attr_dict['created_at'], '%Y-%m-%d %H:%M:%S.%f')

        if 'updated_at' in attr_dict:
            if not isinstance(attr_dict['updated_at'], datetime):
                attr_dict['updated_at'] = datetime.strptime(
                    attr_dict['updated_at'], '%Y-%m-%d %H:%M:%S.%f')

        if attr_dict['__class__']:
            attr_dict.pop('__class__')
        for attr, val in attr_dict.items():
            setattr(self, attr, val)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save_object_from_dict(self, name, value):
        """
            updates the basemodel and sets the correct attributes
        """
        setattr(self, name, value)
        self.save()

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def __is_serializable(self, obj_v):
        """
            private: checks if object is serializable
        """
        try:
            obj_to_str = json.dumps(obj_v)
            return obj_to_str is not None and isinstance(obj_to_str, str)
        except:
            return False


    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        for key, value in (self.__dict__).items():
            if key == '_sa_instance_state':
                del key
            if (self.__is_serializable(value)):
                dictionary[key] = value
            else:
                dictionary[key] = str(value)
        dictionary['__class__'] = type(self).__name__
        return dictionary
    
    def delete(self):
        models.storage.delete(self)
