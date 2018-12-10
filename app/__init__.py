# -*-coding: utf-8-*-
from flask import Flask
from config import config
from models import db


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # TODO(Linx) import bluprint then register in app.
    from login import login as login_blueprint
    app.register_blueprint( login_blueprint, url_prefix='/api/v1/login')

    db.init_app(app)
    return app