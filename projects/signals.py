# projects/signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Task, TaskComment, TaskAttachment
from notifications.models import Notification

User = get_user_model()

@receiver(post_save, sender=Task)
def test_task_signal(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.assigned_to,
            message=f"Test signal: Task '{instance.title}' created!"
        )

# --- helpers -------------------------------------------------
def _notify(recipients, message):
    """Create notifications for unique, non-null recipients."""
    seen = set()
    for user in recipients:
        if user and user.pk and user.pk not in seen:
            Notification.objects.create(recipient=user, message=message)
            seen.add(user.pk)

# --- track old fields before save ----------------------------
@receiver(pre_save, sender=Task)
def _stash_old_task_values(sender, instance: Task, **kwargs):
    if not instance.pk:
        instance._old_status = None
        instance._old_assigned_to_id = None
        return
    try:
        old = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        instance._old_status = None
        instance._old_assigned_to_id = None
        return
    instance._old_status = old.status
    instance._old_assigned_to_id = old.assigned_to_id

# --- Task created / updated ---------------------------------
@receiver(post_save, sender=Task)
def _task_notifications(sender, instance: Task, created, **kwargs):
    project_owner = instance.project.owner
    assignee = instance.assigned_to

    if created:
        # Assignment on create
        if assignee:
            _notify([assignee], f"You were assigned to task '{instance.title}'.")
        return

    # Assignment changed
    if hasattr(instance, "_old_assigned_to_id") and instance.assigned_to_id != instance._old_assigned_to_id:
        new_assignee = assignee
        if new_assignee:
            _notify([new_assignee], f"You were assigned to task '{instance.title}'.")
        # (Optional) notify previous assignee they were unassigned
        if instance._old_assigned_to_id and instance._old_assigned_to_id != (new_assignee.id if new_assignee else None):
            try:
                old_user = User.objects.get(pk=instance._old_assigned_to_id)
                _notify([old_user], f"You were unassigned from task '{instance.title}'.")
            except User.DoesNotExist:
                pass

    # Status changed
    if hasattr(instance, "_old_status") and instance._old_status and instance.status != instance._old_status:
        msg = f"Task '{instance.title}' status changed from {instance._old_status} to {instance.status}."
        # owner + assignee (dedup handled by _notify)
        _notify([project_owner, assignee], msg)

# --- New comment ---------------------------------------------
@receiver(post_save, sender=TaskComment)
def _comment_notifications(sender, instance: TaskComment, created, **kwargs):
    if not created:
        return
    task = instance.task
    project_owner = task.project.owner
    assignee = task.assigned_to
    snippet = (instance.content or "").strip()
    snippet = (snippet[:47] + "...") if len(snippet) > 50 else snippet
    msg = f"New comment on '{task.title}': {snippet}"
    _notify([project_owner, assignee], msg)

# --- Attachment uploaded (optional but handy) ----------------
@receiver(post_save, sender=TaskAttachment)
def _attachment_notifications(sender, instance: TaskAttachment, created, **kwargs):
    if not created:
        return
    task = instance.task
    msg = f"New attachment added to '{task.title}': {instance.file.name.split('/')[-1]}"
    _notify([task.project.owner, task.assigned_to], msg)
