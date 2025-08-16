from celery import shared_task
import time
import logging

logger = logging.getLogger("django")

@shared_task(bind=True, max_retries=3)
def send_task_notification(self, task_id, user_email):
    try:
        time.sleep(3)  # simulate heavy work
        logger.info(f"📩 Notification sent for Task {task_id} to {user_email}")
        return f"Notification sent to {user_email}"
    except Exception as e:
        logger.error(f"Task notification failed: {str(e)}")
        raise self.retry(exc=e, countdown=5)  # retry after 5s
