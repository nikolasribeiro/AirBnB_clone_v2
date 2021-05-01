#!/usr/bin/python3
"""
Write a script that starts a Flask web application:

Your web application must be listening on 0.0.0.0, port 5000
Routes:
/: display “Hello HBNB!”
/hbnb: display “HBNB”
/c/<text>: display “C ”, followed by the value of the text
variable (replace underscore _ symbols with a space)
/python/(<text>): display “Python ”, followed by the value of the text
variable (replace underscore _ symbols with a space)
The default value of text is “is cool”
/number/<n>: display “n is a number” only if n is an integer
/number_template/<n>: display a HTML page only if n is an integer:
H1 tag: “Number: n” inside the tag BODY
/number_odd_or_even/<n>: display a HTML page only if n is an integer:
H1 tag: “Number: n is even|odd” inside the tag BODY
"""
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """ Display the site index
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Display the site hbnb
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """ Display the site with input value of variable
    """
    return "C " + text.replace("_", " ")


@app.route('/python/')
@app.route('/python/<text>', strict_slashes=False)
def python(text='is cool'):
    """ Display the site index
    """
    return "Python " + text.replace("_", " ")


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """ Display the site number parameter
    """
    return str(n) + " is a number "


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """ Display the number in page html
    """
    return render_template('5-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """ Display the odd or even in page html
    """
    return render_template('6-number_odd_or_even.html', number=n)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
