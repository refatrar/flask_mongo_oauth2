from flask import request
from flask_restful import Resource
from flask_mongoengine.wtf import model_form
import hashlib

from application.model.schemaModel import Users
from application.middleware.auth import is_client_authenticate, is_user_authenticate
from application.services.resService import ResService
from application.services.authService import AUTH
from application.services.logService import LOG


# User Registration
class Signup(Resource):
    @is_client_authenticate()
    def post(self):
        try:
            body = request.form.to_dict(flat=True)

            PostForm = model_form(Users)
            form = PostForm(request.form, csrf_enabled=False)

            if request.method == 'POST' and form.validate():
                email_exists = Users.objects(email=body['email'])
                if email_exists:
                    return ResService.not_acceptable('This email is already taken for another tutor!'), \
                           ResService.not_acceptable()['status']

                body['password'] = hashlib.md5(body['password'].encode('utf-8')).hexdigest()
                save_data = Users(**body).save()

                if save_data:
                    user_info = {
                        'user_info': {
                            'user_id': str(save_data.id),
                            'name': body['name'],
                            'email': body['email']
                        }
                    }

                    return ResService.created('Welcome!',
                                              dict(AUTH.generate_tokens(str(save_data.id)), **user_info)
                                              ), ResService.created()['status']
            else:
                errors = form.errors
                return ResService.validation_response(errors), ResService.validation_response()['status']
        except Exception as err:
            LOG.report(err)
            return ResService.bad_request(), ResService.bad_request()['status']


# User Login
class Login(Resource):
    @is_client_authenticate()
    def post(self):
        try:
            body = request.form.to_dict(flat=True)

            PostForm = model_form(Users, exclude=['name', 'confirm'])
            form = PostForm(request.form, csrf_enabled=False)

            if request.method == 'POST' and form.validate():
                find_user = Users.objects(email=body['email']).first()

                if find_user:
                    if hashlib.md5(body['password'].encode('utf-8')).hexdigest() != find_user['password']:
                        return ResService.not_acceptable('Invalid email or password!'), \
                               ResService.not_acceptable()['status']

                    user_info = {
                        'user_info': {
                            'user_id': str(find_user.id),
                            'name': find_user.name,
                            'email': find_user.email
                        }
                    }

                    return ResService.created('Welcome!',
                                              dict(AUTH.generate_tokens(str(find_user['id'])), **user_info)
                                              ), ResService.created()['status']
                else:
                    return ResService.not_acceptable('You do not have an account on our system with this email!'), \
                           ResService.not_acceptable()['status']
            else:
                errors = form.errors
                return ResService.validation_response(errors), ResService.validation_response()['status']
        except Exception as err:
            LOG.report(err)
            return ResService.bad_request(), ResService.bad_request()['status']


class Signout(Resource):
    @is_user_authenticate()
    def delete(self):
        try:
            AUTH.sign_out()
            return ResService.deleted('Signout Successful!'), ResService.deleted()['status']

        except Exception as err:
            LOG.report(err)
            return ResService.bad_request(), ResService.bad_request()['status']


