# notifications/repositories.py

from ..models import Notification

class NotificationRepository:
    """
    Repository for Notification model.
    Handles all database-level operations.
    """

    @staticmethod
    def get_user_notifications(user):
        """
        Fetch all notifications for a user, newest first.
        """
        return Notification.objects.filter(recipient=user).order_by('-created_at')

    @staticmethod
    def get_notification_by_id(pk):
        """
        Retrieve a single notification by primary key.
        """
        return Notification.objects.get(pk=pk)

    @staticmethod
    def create_notification(recipient, message):
        """
        Create a new notification.
        """
        return Notification.objects.create(recipient=recipient, message=message)

    @staticmethod
    def mark_as_read(notification):
        """
        Mark a notification as read.
        """
        notification.is_read = True
        notification.save()
        return notification
