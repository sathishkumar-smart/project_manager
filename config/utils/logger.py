# utils/logger.py

import os
import logging
from django.conf import settings

def custom_log(message, file_path="custom.log", level="info"):
    """
    Write logs into a custom file.
    Example file_path: 'task/comment/update.log'
    """
    # Ensure directory exists
    log_file_path = os.path.join(settings.LOG_DIR, file_path)
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # Create logger
    logger = logging.getLogger(file_path)
    handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Avoid duplicate handlers
    if not logger.handlers:
        logger.addHandler(handler)
    
    # Log according to level
    getattr(logger, level)(message)
