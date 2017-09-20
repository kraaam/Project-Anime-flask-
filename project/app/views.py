
from flask import render_template

from app import app


def create_app(config_name):
    # existing code remains

    # temporary route
    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    return app