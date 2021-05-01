#!/usr/bin/python3
""" Display into webpage 
"""
from flask import Flask, render_template
import models
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.user import User
app = Flask(__name__)


@app.teardown_appcontext
def storage_close(self):
    """ Module for remove the SQLAlchemy Session. 
    """
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """ Display into webpage 
    """
    value_state = storage.all(State).values()
    value_amenity = storage.all(Amenity).values()
    value_place = storage.all(Place).values()
    #value_users = storage.all(User).values()
    value_users = storage.all(User)
    return render_template(
        '100-hbnb.html', states=value_state,
        amenities=value_amenity, places=value_place, users=value_users)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
