import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-my-key'
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))