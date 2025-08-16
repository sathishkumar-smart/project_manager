# config/logging_handlers.py
import logging

class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        try:
            from notifications.models import LogEntry   # <-- moved inside
            LogEntry.objects.create(
                level=record.levelname,
                message=self.format(record),
                logger_name=record.name,
            )
        except Exception:
            # Prevent infinite loops if DB write fails
            pass
