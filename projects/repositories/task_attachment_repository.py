"""
attachment_repository.py

Repository layer for managing TaskAttachment persistence.
This layer is responsible for all database operations 
related to file attachments in tasks.

Responsibilities:
1. Create new task attachments.
2. Retrieve attachments for a task, scoped to the project owner.
"""

from projects.models import TaskAttachment


class AttachmentRepository:
    """
    Repository class for interacting with the TaskAttachment model.
    Encapsulates all database queries and mutations related to task attachments.
    """

    @staticmethod
    def create_attachment(**kwargs):
        """
        Create a new task attachment.

        Args:
            **kwargs: Fields required for creating a TaskAttachment instance 
                      (e.g., `task`, `file`, `uploaded_by`, etc.).

        Returns:
            TaskAttachment: The created TaskAttachment instance.
        """
        return TaskAttachment.objects.create(**kwargs)

    @staticmethod
    def get_task_attachments(task_id, user):
        """
        Retrieve all attachments for a given task, restricted by project ownership.

        Args:
            task_id (int): The ID of the task.
            user (User): The user requesting the attachments. 
                         Ensures they are the project owner.

        Returns:
            QuerySet: A queryset of TaskAttachment objects.
        """
        return TaskAttachment.objects.filter(
            task_id=task_id,
            task__project__owner=user
        )
