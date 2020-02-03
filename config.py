import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-my-key'
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('RESUME_DATABASE_URI') or \
        'sqlite:///' + os.path.join(base_dir,'resume_database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False