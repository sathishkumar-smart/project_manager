"""
task_service.py

This service layer manages task-related operations.
It separates business logic from views and delegates database access
to the TaskRepository.

Responsibilities:
1. Create tasks and assign them to users (with notifications + email).
2. Update task details (with validation for status and permissions).
3. Retrieve comments for a given task (with caching).
"""

from notifications.models import Notification
from projects.tasks import send_task_assignment_email
from projects.repositories.task_repository import TaskRepository
from config.utils.logger import custom_log
from config.exceptions import InvalidTaskStatus
from rest_framework.exceptions import PermissionDenied, APIException
from django.core.cache import cache


class TaskService:
    """
    Service class for handling business logic related to tasks.
    """

    @staticmethod
    def create_task(serializer, request):
        """
        Create a new task and optionally notify the assigned user.

        Workflow:
        1. Assign the task to the selected user (or fallback to the creator).
        2. Save the task using TaskRepository.
        3. If the task is assigned:
            - Create an in-app notification.
            - Send an async email notification.
        4. Log and raise an APIException if anything fails.

        Args:
            serializer (Serializer): DRF serializer with validated task data.
            request (Request): The current request object (contains user).

        Returns:
            Task: The newly created Task instance.

        Raises:
            APIException: If task creation fails unexpectedly.
        """
        assigned_user = serializer.validated_data.get("assigned_to") or request.user
        try:
            task = TaskRepository.create_task(
                assigned_to=assigned_user,
                created_by=request.user,
                **serializer.validated_data
            )

            # Send notifications if assigned
            if task.assigned_to:
                Notification.objects.create(
                    recipient=task.assigned_to,
                    message=f"You have been assigned to task '{task.title}'"
                )
                send_task_assignment_email.delay(task.id, task.assigned_to.email)

            return task
        except Exception as e:
            custom_log(
                f"Error creating task: {str(e)}",
                file_path="task/comment/update.log",
                level="error"
            )
            raise APIException("Failed to create task. Please try again.")

    @staticmethod
    def update_task(serializer, request):
        """
        Update a task (status, assigned user, etc.) with validation.

        Validations:
        - Only allow valid status transitions: ['todo', 'in_progress', 'completed'].
        - Prevent non-staff users from reassigning tasks.

        Args:
            serializer (Serializer): DRF serializer with validated task data.
            request (Request): The current request object (contains user and data).

        Returns:
            Task: The updated Task instance.

        Raises:
            InvalidTaskStatus: If the provided status is invalid.
            PermissionDenied: If a non-staff user tries to reassign a task.
        """
        status_value = request.data.get("status")
        if status_value not in ['todo', 'in_progress', 'completed']:
            raise InvalidTaskStatus()

        if request.data.get("assigned_to") and not request.user.is_staff:
            raise PermissionDenied("You can't reassign tasks to others.")

        return serializer.save()

    @staticmethod
    def get_comments(user, task_id):
        """
        Retrieve comments for a task with caching.

        Workflow:
        1. Try fetching comments from cache.
        2. If not cached, query from TaskRepository.
        3. Store results in cache for 10 minutes.

        Args:
            user (User): The user requesting the comments.
            task_id (int): The task ID for which comments are retrieved.

        Returns:
            QuerySet: A queryset of TaskComment objects.
        """
        cache_key = f"user_{user.id}_task_{task_id}_comments"
        comments = cache.get(cache_key)
        if not comments:
            comments = TaskRepository.get_task_comments(task_id, user)
            cache.set(cache_key, comments, timeout=60 * 10)
        return comments
