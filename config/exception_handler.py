# project_manager/core/exception_handler.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Custom global exception handler for DRF.
    Ensures all errors return a consistent JSON format.
    """
    # Let DRF handle the default first
    response = exception_handler(exc, context)

    if response is not None:
        # Log the error
        logger.error(f"Exception: {exc} | Context: {context}")

        # Customize the error format
        return Response(
            {
                "success": False,
                "error": {
                    "type": exc.__class__.__name__,
                    "message": response.data.get("detail", str(exc)),
                }
            },
            status=response.status_code
        )

    # For unhandled exceptions
    logger.critical(f"Unhandled Exception: {exc} | Context: {context}")
    return Response(
        {
            "success": False,
            "error": {
                "type": exc.__class__.__name__,
                "message": str(exc)
            }
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
