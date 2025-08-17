from django.db import models
from django.conf import settings


class Notification(models.Model):
    """
    Model to store user notifications.
    Each notification belongs to a recipient user.
    """
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'  # Allows user.notifications.all() access
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)  # Track if the notification was read
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when created

    def __str__(self):
        # Display first 30 characters of the message for readability
        return f"Notification to {self.recipient.email} - {self.message[:30]}"

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']  # Newest notifications first


class LogEntry(models.Model):
    """
    Model to store application logs.
    Useful for debugging, monitoring, and auditing.
    """
    level = models.CharField(max_length=20)  # e.g., INFO, ERROR, WARNING
    message = models.TextField()
    logger_name = models.CharField(max_length=50)  # Name of the logger
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of the log

    class Meta:
        db_table = 'db_logs'  # Correct way to set custom table name
        ordering = ['-created_at']  # Show latest logs first
        verbose_name = 'Log Entry'
        verbose_name_plural = 'Log Entries'

    def __str__(self):
        # Display a concise summary for admin or debug views
        return f"[{self.level}] {self.logger_name}: {self.message[:50]}"
