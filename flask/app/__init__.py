
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from app import dbroutes

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'fipubot'
app.config['MONGO_URI'] = 'mongodb+srv://admin:<F1pub0t!>@fipubot.mfio0.mongodb.net/fipubot?retryWrites=true&w=majority'
app.config['JWT_SECRET_KEY'] = 'secret'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app, resources={r'/*': {'origins': '*'}})

if __name__ == '__main__':
    app.run()

#getMessages
#getRooms
#getUsers
#getFiles

# SHOPPING_LIST = [
#     {
#         'name': 'olive oil',
#         'quantity': 1,
#         'unit': 'bottle(s)',
#         'missing': True,
#     },
#     {
#         'name': 'mozzarella cheese',
#         'quantity': 250,
#         'unit': 'g',
#         'missing': True,
#     },
#     {
#         'name': 'tomatoes',
#         'quantity': 200,
#         'unit': 'g',
#         'missing': True,
#     },
#     {
#         'name': 'basil',
#         'quantity': 75,
#         'unit': 'g',
#         'missing': True,
#     }
# ]
# @app.route('/shoppinglist', methods=['GET', 'POST'])
# def index():
#     response_dict = {
#         'status': 'success',
#         'message': '',
#         'shopping_list': SHOPPING_LIST
#     }

#     if request.method == 'POST':
#         # update shopping list
#         SHOPPING_LIST.clear()
#         SHOPPING_LIST.extend(request.get_json())
#         response_dict['message'] = 'List updated'
#     else:
#         # return default list
#         response_dict['message'] = 'List aquired'

#     return jsonify(response_dict)