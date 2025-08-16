import time
import json
import logging
from django.utils.deprecation import MiddlewareMixin

api_logger = logging.getLogger('api_logger')

class APILoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        duration = round(time.time() - getattr(request, "start_time", time.time()), 4)
        user = request.user if request.user.is_authenticated else "Anonymous"

        log_data = {
            "user": str(user),
            "method": request.method,
            "path": request.get_full_path(),
            "status": response.status_code,
            "duration": f"{duration}s"
        }

        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                log_data["body"] = json.loads(request.body.decode("utf-8"))
            except Exception:
                log_data["body"] = "unreadable"

        api_logger.info(json.dumps(log_data))
        return response
