"""
Sometimes in your Django model you want to raise a ``ValidationError`` in the ``save`` method, for
some reason.
This exception is not managed by Django Rest Framework because it occurs after its validation 
process. So at the end, you'll have a 500.
Correcting this is as simple as overriding the exception handler, by converting the Django
``ValidationError`` to a DRF one.
"""
import logging
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import exception_handler as drf_exception_handler

LOG = logging.getLogger(__name__)


# def exception_handler(exc, context):
def exception_handler(exc, context):
    """
    Handle Django ValidationError as an accepted exception
    Must be set in settings:
    >>> REST_FRAMEWORK = {
    ...     # ...
    ...     "EXCEPTION_HANDLER": "api.exception_handler.exception_handler",
    ...     # ...
    ... }
    """

    if isinstance(exc, DjangoValidationError):
        if hasattr(exc, "message_dict"):
            detail = {"error": exc.message_dict}
        elif hasattr(exc, "message"):
            detail = {"error": exc.message}
        elif hasattr(exc, "messages"):
            detail = {"error": exc.messages}
        else:
            LOG.error("Unhandled validation message: %s", exc)

        exc = DRFValidationError(detail=detail)

    return drf_exception_handler(exc, context)
