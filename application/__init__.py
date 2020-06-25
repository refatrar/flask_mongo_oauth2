from flask import Flask
from flask_cors import CORS
from application.config import Config

from application.routes.api import api_bp
from application.mongodb import initialize_db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    initialize_db(app)

    CORS(app)

    app.register_blueprint(api_bp)

    return app
