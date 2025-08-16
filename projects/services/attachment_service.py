"""
attachment_service.py

This service layer encapsulates business logic for handling task attachments.  
It acts as an intermediary between the views and the repository layer, ensuring that:
- ViewSets stay thin (only delegate work)
- Repository handles database access
- Services handle orchestration of logic (e.g., permission checks, defaults, transformations)

Responsibilities:
1. Listing attachments for a given task (scoped to a user).
2. Creating new attachments tied to a specific task and user.
"""

from ..repositories.task_attachment_repository import AttachmentRepository


class AttachmentService:
    """
    Service class for managing task attachments.
    """

    @staticmethod
    def list_attachments(user, task_id):
        """
        Retrieve all attachments related to a specific task, filtered by user.

        Args:
            user (User): The currently authenticated user.
            task_id (int): ID of the task to fetch attachments for.

        Returns:
            QuerySet: A queryset of TaskAttachment objects.
        """
        return AttachmentRepository.get_task_attachments(task_id, user)

    @staticmethod
    def create_attachment(serializer, task_id, user):
        """
        Create a new task attachment associated with a given task and user.

        Args:
            serializer (Serializer): DRF serializer instance with validated data.
            task_id (int): The task to which the attachment belongs.
            user (User): The user uploading the attachment.

        Returns:
            TaskAttachment: The newly created TaskAttachment object.
        """
        return serializer.save(task_id=task_id, uploaded_by=user)
