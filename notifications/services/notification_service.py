# notifications/services.py

from ..repositories.notifications_repository import NotificationRepository

class NotificationService:
    """
    Service layer for Notifications.
    Handles business logic separate from views.
    """

    @staticmethod
    def list_user_notifications(user):
        """
        Return all notifications for a user.
        """
        return NotificationRepository.get_user_notifications(user)

    @staticmethod
    def create_user_notification(user, message):
        """
        Create a notification for a user.
        """
        return NotificationRepository.create_notification(user, message)

    @staticmethod
    def mark_notification_as_read(notification):
        """
        Mark a notification as read.
        """
        return NotificationRepository.mark_as_read(notification)
