from flask import request, jsonify
from flask_restful import Resource

from application.middleware.auth import is_user_authenticate
from application.model.schemaModel import AuthAccessTokens
from application.services.resService import ResService


# User Information
class UserData(Resource):
    @staticmethod
    @is_user_authenticate()
    def get():
        user_info = AuthAccessTokens.objects.filter(
            access_token=request.headers.get('Authorization').split(' ')[1]).aggregate([
            {
                "$lookup": {
                    "from": "users",
                    "let": {"userId": "$userid"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$eq": ["$userid", "$$userId"]
                                }
                            }
                        },
                        {
                            "$project": {
                                "ID": 1,
                                "name": 1,
                                "email": 1
                            }
                        }
                    ],
                    "as": "userinfo"
                }
            },
            {
                "$unwind": "$userinfo"
            }
        ])

        user_data = list(user_info)[0]['userinfo']
        user_data['_id'] = str(user_data['_id'])

        return ResService.created('User Info',
                                  user_data
                                  ), ResService.created()['status']