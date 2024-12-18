from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class ConflictError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('Entity already exists.')
    default_code = 'conflict_error'
