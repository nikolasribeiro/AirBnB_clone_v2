#!/usr/bin/python3
"""
List states
"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def teardown(self):
    """ Tear down close storage
    """
    storage.close()


@app.route('/states_list')
def states_list():
    """ Display list state
    """
    states = storage.all(State).values()

    return render_template('7-states_list.html', list=states)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
