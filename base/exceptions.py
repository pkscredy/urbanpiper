from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class CustomAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'An unknown API Exception occurred.'
    default_code = 'unknown_api_error'

    def __init__(self, message=None, error_dict=None, code=None):
        message = _(message or self.default_detail)
        self.code = code or self.default_code

        super(CustomAPIException, self).__init__(detail=message,
                                                 code=self.code)
        self.message = message
        self.error_dict = error_dict or {}


class ModelOperationError(CustomAPIException,
                          ObjectDoesNotExist,
                          IntegrityError):
    """
    Exception raised when any db operation does something insane.
    """
    default_detail = 'A Model Operation Error occurred.'
    default_code = 'model_operation_error'


class SuppressedAPIException(CustomAPIException):
    """
    Exception raised for invalid checksum.
    """
    default_detail = 'An user error occurred.'
    default_code = 'user_error'

# class ChoicesError(SuppressedAPIException):
#     """
#     Exception raised while parsing choices.
#     """
#     default_detail = 'Invalid Choice.'
#     default_code = 'choice_error'
