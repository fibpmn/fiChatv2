from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config(object):
    MONGO_DBNAME = "fipubot"
    MONGO_URI = environ.get('MONGO_URI')
    #JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')

class ProdConfig(object):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    MONGO_URI = environ.get('MONGO_URI')