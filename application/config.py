import os


class Config:
    BUNDLE_ERRORS = True
    MONGODB_SETTINGS = {
        'host': 'mongodb://127.0.0.1:27017/flask_oauth'
    }
    SECRET_KEY = os.environ.get('SECRET_KEY')