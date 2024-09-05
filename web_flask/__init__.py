#!/usr/bin/python3
"""
Init file for web_flask.
"""
from flask import Flask

def create_app():
    """Creates a Flask application instance."""
    app = Flask(__name__)
    return app
