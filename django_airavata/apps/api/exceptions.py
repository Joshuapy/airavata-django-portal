import json
import logging

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from thrift.Thrift import TException

from airavata.api.error.ttypes import AiravataSystemException

log = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    log.debug("API exception", exc_info=exc)
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Default TException handler, should come after more specific subclasses of
    # TException
    if isinstance(exc, TException):
        log.error("TException", exc_info=exc)
        return Response(
            {'detail': str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Generic handler
    if response is None:
        return Response(
            {'detail': str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    if isinstance(exc, serializers.ValidationError):
        # Create a default error message for the validation error
        response.data['detail'] = "ValidationError: {}".format(
            json.dumps(response.data))

    return response