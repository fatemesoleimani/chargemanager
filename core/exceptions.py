from rest_framework.exceptions import APIException
from rest_framework import status


class NotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Object not found"
    default_code = "not_found"


class InvalidStateException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid state for this operation"
    default_code = "invalid_state"
