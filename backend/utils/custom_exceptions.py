from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.data.get('detail').code

    return response


class Unauthenticated(APIException):
    status_code = 200
    default_detail = 'Unauthenticated'
    default_code = '600'


class MustChangeInitPassword(APIException):
    status_code = 200
    default_detail = 'User must change init password'
    default_code = '601'


class ValidationError(APIException):
    status_code = 200
    default_detail = 'The input value is invalid'
    default_code = '602'


class InvalidToken(APIException):
    status_code = 200
    default_detail = 'Invalid token'
    default_code = '603'


class TokenExpired(APIException):
    status_code = 200
    default_detail = 'Token expired'
    default_code = '604'


class ObjectNotFound(APIException):
    status_code = 200
    default_detail = 'Not found'
    default_code = '605'
