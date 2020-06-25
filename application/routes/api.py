from flask import Blueprint
from flask_restful import Api

# Import Controller Class
from application.controllers.authentication import Signup, Login, Signout
from application.controllers.user import UserData

# Blueprint
api_bp = Blueprint('api', __name__)
api = Api(api_bp)


api.add_resource(Signup, '/signup')
api.add_resource(Login, '/signin')
api.add_resource(UserData, '/userinfo')
api.add_resource(Signout, '/signout')