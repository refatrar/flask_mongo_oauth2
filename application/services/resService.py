import json
from datetime import datetime, timedelta, date


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return str(o)
        if isinstance(o, timedelta):
            return str(o)
        if isinstance(o, date):
            return str(o)
        return json.JSONEncoder.default(self, o)


class ResService:
    def __init__(self, params):
        self.params = params

    @staticmethod
    def validation_response(message=None):
        return ResService.error_response(422, message)

    @staticmethod
    def json_formatter(data):
        return json.loads(JSONEncoder().encode(data))

    @staticmethod
    def unauthorized(message='Unauthorized or Session Destroyed'):
        return ResService.error_response(401, message)

    @staticmethod
    def success_response(status, message, data):
        return {'status': status, 'message': message, 'data': data}

    @staticmethod
    def error_response(status, message):
        return {'status': status, 'message': message}

    @staticmethod
    def success(message=None, data=None):
        return ResService.success_response(200, message, data)

    @staticmethod
    def created(message='Data Inserted', data=None):
        return ResService.success_response(201, message, data)

    @staticmethod
    def updated(message='Data Updated', data=None):
        return ResService.success_response(202, message, data)

    @staticmethod
    def deleted(message='Data Deleted', data=None):
        return ResService.success_response(202, message, data)

    @staticmethod
    def not_acceptable(message='Something Went Wrong'):
        return ResService.error_response(406, message)

    @staticmethod
    def no_content(message='No Data Found', data=None):
        return ResService.success_response(204, message, data)

    @staticmethod
    def bad_request(message='Something Went Wrong'):
        return ResService.error_response(400, message)