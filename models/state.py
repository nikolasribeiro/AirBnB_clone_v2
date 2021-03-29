#!/usr/bin/python3
"""This is the state class"""
import os
from sqlalchemy import Column, Integer, String, ForeignKey
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from models.city import City


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = "states"

    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state",
                          cascade="all, delete-orphan")

    if os.getenv("HBNB_TYPE_STORAGE") == "fs":
        @property
        def cities(self):
            """ Returns list of City instance with equal state_id """
            from models import storage
            my_list = []
            for city in storage.all("City").values():
                if city.state_id == self.id:
                    my_list.append(city)
            return my_list
