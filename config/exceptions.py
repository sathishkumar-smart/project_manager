# project_manager/core/exceptions.py
from rest_framework.exceptions import APIException

class InvalidTaskStatus(APIException):
    status_code = 400
    default_detail = "Invalid task status."
    default_code = "invalid_task_status"

class PermissionDeniedCustom(APIException):
    status_code = 403
    default_detail = "You do not have permission to perform this action."
    default_code = "permission_denied_custom"

class ResourceNotFound(APIException):
    status_code = 404
    default_detail = "The requested resource was not found."
    default_code = "resource_not_found"
