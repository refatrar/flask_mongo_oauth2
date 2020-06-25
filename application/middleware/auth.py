from flask import request
from functools import wraps

from application.model.schemaModel import AuthClients, AuthAccessTokens
from application.services.resService import ResService


def is_client_authenticate():
    def _is_client_authenticate(f):
        @wraps(f)
        def __is_client_authenticate(*args, **kwargs):
            if request.authorization:
                iscLient = AuthClients.objects(name=request.authorization.username, secret=request.authorization.password).first()

                if iscLient and 'name' in iscLient and 'secret' in iscLient:
                    result = f(*args, **kwargs)
                    return result
                else:
                    return ResService.not_acceptable('Invalid Request'), ResService.not_acceptable()['status']
            else:
                return ResService.not_acceptable('Invalid Request'), ResService.not_acceptable()['status']
        return __is_client_authenticate
    return _is_client_authenticate


def is_user_authenticate():
    def _is_user_authenticate(f):
        @wraps(f)
        def __is_user_authenticate(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if auth_header:
                access_token = auth_header.split(' ')[1]

                user_info = AuthAccessTokens.objects(access_token=access_token).first()
                if user_info:
                    result = f(*args, **kwargs)
                    return result
                else:
                    return ResService.unauthorized('Token Expired'), ResService.unauthorized()['status']
            else:
                return ResService.unauthorized('Invalid Token'), ResService.unauthorized()['status']

        return __is_user_authenticate

    return _is_user_authenticate
