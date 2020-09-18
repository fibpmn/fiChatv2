from flask import Flask
from config import Config
from flask_cors import CORS
app = Flask(__name__)

cors = CORS()
cors.init_app(app)
app.config.from_object('config.Config')

from app import dbroutes, bpmnroutes, camundarest, xmlparser, auth, externals, dbparser

