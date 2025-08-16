"""
comment_repository.py

Repository layer for managing TaskComment persistence.
This module encapsulates all database operations 
related to task comments.

Responsibilities:
1. Create new task comments.
2. Retrieve comments for a task, scoped to the project owner.
"""

from projects.models import TaskComment


class CommentRepository:
    """
    Repository class for interacting with the TaskComment model.
    Provides an abstraction layer for comment-related database queries.
    """

    @staticmethod
    def create_comment(**kwargs):
        """
        Create a new task comment.

        Args:
            **kwargs: Fields required for creating a TaskComment instance
                      (e.g., `task`, `author`, `content`, etc.).

        Returns:
            TaskComment: The created TaskComment instance.
        """
        return TaskComment.objects.create(**kwargs)

    @staticmethod
    def get_task_comments(task_id, user):
        """
        Retrieve all comments for a given task, restricted by project ownership.

        Args:
            task_id (int): The ID of the task.
            user (User): The user requesting the comments. 
                         Ensures they are the project owner.

        Returns:
            QuerySet: A queryset of TaskComment objects.
        """
        return TaskComment.objects.filter(
            task_id=task_id,
            task__project__owner=user
        )
