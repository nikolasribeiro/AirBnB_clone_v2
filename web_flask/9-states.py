#!/usr/bin/python3
"""
cities by state
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
app = Flask(__name__)


@app.teardown_appcontext
def teardown(self):
    """ close files storage
    """
    storage.close()


@app.route('/states_list', strict_slashes=False)
@app.route('/states', strict_slashes=False)
def states():
    """ display states in html page
    """
    context = storage.all(State).values()
    print(context)
    return render_template('7-states_list.html', states=context)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """ display state in html page
    """
    states = storage.all(State)
    key = 'State.{}'.format(id)
    if key in states:
        state = states[key]
    else:
        state = None
    return render_template('9-states.html', state=state)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
