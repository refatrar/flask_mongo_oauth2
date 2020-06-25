from flask import request
from bcrypt import hashpw, gensalt
from datetime import datetime, timedelta
from bson.objectid import ObjectId

from application.services.resService import ResService
from application.model.schemaModel import AuthClients, Users, AuthAccessTokens, AuthRefreshTokens
from application.services.logService import LOG


class AUTH:
    @staticmethod
    def generate_tokens(user_id):
        try:
            data = {
                'access_token': {
                    'token': (hashpw(str('accessToken').encode('UTF_8') + str(datetime.now()).encode('UTF_8') + user_id.encode('UTF_8'), gensalt())).decode('ascii'),
                    'created_at': datetime.today(),
                    'expired_at': datetime.today() + timedelta(minutes=720)
                },
                'refresh_token': {
                    'token': (hashpw(str('refreshToken').encode('UTF_8') + str(datetime.now()).encode('UTF_8') + user_id.encode('UTF_8'), gensalt())).decode('ascii'),
                    'created_at': datetime.today(),
                    'expired_at': datetime.today() + timedelta(minutes=4320)
                }
            }

            if request.authorization:
                find_client = AuthClients.objects(name=request.authorization.username).first()

                if find_client and ObjectId(find_client['id']):
                    access_token_data = {
                        'access_token': data['access_token']['token'],
                        'client_id': ObjectId(find_client['id']),
                        'user_id': user_id,
                        'expired_at': data['access_token']['expired_at'],
                        'created_at': data['access_token']['created_at']
                    }

                    access_token = AuthAccessTokens(**access_token_data).save()
                    access_token_id = access_token.id
                    if str(access_token_id):
                        refresh_token_data = {
                            'access_token_id': str(access_token_id),
                            'refresh_token': data['refresh_token']['token'],
                            'client_id': find_client['id'],
                            'user_id': user_id,
                            'expired_at': data['refresh_token']['expired_at'],
                            'created_at': data['refresh_token']['created_at']
                        }
                        AuthRefreshTokens(**refresh_token_data).save()

                        return ResService.json_formatter(data)
                    else:
                        return ResService.json_formatter(data)
                else:
                    return ResService.json_formatter(data)
            else:
                return ResService.json_formatter(data)

        except Exception as err:
            LOG.report(err)

    @staticmethod
    def sign_out():
        try:
            find_token = AuthAccessTokens.objects(
                access_token=request.headers.get('Authorization').split(' ')[1]).first()
            AuthRefreshTokens.objects(access_token_id=find_token.id).delete()
            find_token.delete()
            return True
        except Exception as err:
            LOG.report(err)