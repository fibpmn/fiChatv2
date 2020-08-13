from flask import Flask
from config import Config
from flask_cors import CORS
app = Flask(__name__)

cors = CORS()
cors.init_app(app)
app.config.from_object('config.Config')

from app import dbroutes, bpmnroutes, camundarest

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