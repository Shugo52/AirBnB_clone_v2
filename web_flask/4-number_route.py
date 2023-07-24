#!/usr/bin/python3
"""Starts a Flask web application
Listens on 0.0.0.0, port 5000
Routes:
    /:
        display “Hello HBNB!”
    /hbnb:
        display “HBNB”
    /c/<text>:
        display “C ”, followed by the value of the text variable
        (replace underscore _ symbols with a space )
    /python/(<text>):
        display “Python ”, followed by the value of the text variable
        (replace underscore _ symbols with a space )
        The default value of text is “is cool”
    You must use the option strict_slashes=False in your route definition
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """Displays 'Hello HBNB'"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Displays 'HBNB'"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def display_text(text):
    """Displays 'C', , followed by the value of the text"""
    text = text.replace('_', ' ')
    return f'C {text}'


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text='is cool'):
    """Displays 'Python', , followed by the value of the text"""
    text = text.replace('_', ' ')
    return f'Python {text}'


@app.route('/number/<n>', strict_slashes=False)
def number(n):
    """Displays '<n> is a number' if n is an integer"""
    if isinstance(n, int):
        return f'{n} is a number'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
