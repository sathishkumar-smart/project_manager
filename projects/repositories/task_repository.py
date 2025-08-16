"""
task_repository.py

Repository layer for managing Task persistence and related entities 
(TaskComment, TaskAttachment). 

Responsibilities:
1. Create and update tasks.
2. Retrieve comments related to a specific task (scoped by project owner).
3. (Future scope) Extend with queries for attachments, filters, and status-based retrieval.
"""

from projects.models import Task, TaskComment, TaskAttachment


class TaskRepository:
    """
    Repository class for interacting with the Task model and 
    related entities (comments, attachments).
    Provides an abstraction layer for task-related database queries.
    """

    @staticmethod
    def create_task(**kwargs):
        """
        Create a new task.

        Args:
            **kwargs: Fields required for creating a Task instance
                      (e.g., title, description, assigned_to, created_by, project).

        Returns:
            Task: The created Task instance.
        """
        return Task.objects.create(**kwargs)

    @staticmethod
    def update_task(task, **kwargs):
        """
        Update an existing task with the provided fields.

        Args:
            task (Task): The Task instance to update.
            **kwargs: Fields and values to update (e.g., status, title).

        Returns:
            Task: The updated Task instance.
        """
        for key, value in kwargs.items():
            setattr(task, key, value)
        task.save()
        return task

    @staticmethod
    def get_task_comments(task_id, user):
        """
        Retrieve all comments for a given task, restricted by project ownership.

        Args:
            task_id (int): The ID of the task.
            user (User): The user requesting the comments. 
                         Ensures they are the project owner.

        Returns:
            QuerySet: A queryset of TaskComment objects related to the task.
        """
        return TaskComment.objects.filter(
            task_id=task_id,
            task__project__owner=user
        )
