from flask import Flask
from config import Config
from flask_restful import Api


app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)

from app import routes