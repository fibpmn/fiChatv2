from os import environ, path
from dotenv import load_dotenv
import datetime

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config(object):
    MONGO_DBNAME = "fipubot"
    MONGO_URI = environ.get('MONGO_URI')
    JSONIFY_PRETTYPRINT_REGULAR = True
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    
class ProdConfig(object):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    MONGO_URI = environ.get('MONGO_URI')