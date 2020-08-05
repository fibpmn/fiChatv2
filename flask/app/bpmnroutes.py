from app import app
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo

mongo = PyMongo(app)
CORS(app, resources={r'/*': {'origins': '*'}})