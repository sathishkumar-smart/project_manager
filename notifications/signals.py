# notifications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from projects.models import Task, TaskComment
from .models import Notification

# Notify when a task is assigned
@receiver(post_save, sender=Task)
def notify_task_assignment(sender, instance, created, **kwargs):
    if created and instance.assigned_to:
        Notification.objects.create(
            recipient=instance.assigned_to,
            message=f"You have been assigned to task: {instance.title}"
        )
    elif not created:  # If task updated
        # If status changed
        if 'status' in instance.__dict__ and instance.status:
            Notification.objects.create(
                recipient=instance.assigned_to,
                message=f"Task '{instance.title}' status changed to {instance.status}"
            )

# Notify when a comment is added
@receiver(post_save, sender=TaskComment)
def notify_task_comment(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.task.assigned_to,
            message=f"New comment on task '{instance.task.title}': {instance.content[:50]}"
        )
