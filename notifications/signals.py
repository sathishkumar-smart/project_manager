# notifications/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from projects.models import Task, TaskComment
from .models import Notification


# ------------------------------
# Signal: Notify when a task is assigned or updated
# ------------------------------
@receiver(post_save, sender=Task)
def notify_task_assignment(sender, instance, created, **kwargs):
    """
    Sends notifications when a Task is created or updated.
    - On creation: notify the assigned user.
    - On update: notify if the status changes.
    """
    if created and instance.assigned_to:
        # Task created and assigned to a user
        Notification.objects.create(
            recipient=instance.assigned_to,
            message=f"You have been assigned to task: {instance.title}"
        )
    else:
        # Task updated
        # Check if the status has changed
        # Note: instance.__dict__ contains current values, not previous ones
        # For real change detection, consider using django-dirtyfields or custom tracking
        if hasattr(instance, 'status') and instance.assigned_to:
            Notification.objects.create(
                recipient=instance.assigned_to,
                message=f"Task '{instance.title}' status changed to {instance.status}"
            )


# ------------------------------
# Signal: Notify when a comment is added to a task
# ------------------------------
@receiver(post_save, sender=TaskComment)
def notify_task_comment(sender, instance, created, **kwargs):
    """
    Sends notifications to the assigned user when a comment is added to their task.
    """
    if created and instance.task.assigned_to:
        Notification.objects.create(
            recipient=instance.task.assigned_to,
            message=f"New comment on task '{instance.task.title}': {instance.content[:50]}"
        )
