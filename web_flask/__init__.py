#!/usr/bin/python3
from flask import Flask

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    @app.route('/hello', strict_slashes=False)
    def hello():
        return "Hello HBNB!"

    return app
