"""
comment_service.py

This service layer manages business logic for task comments.  
It ensures views remain thin by handling:
- Fetching task comments with caching for performance.
- Creating new comments tied to a specific task and user.

Responsibilities:
1. Retrieve task comments with caching (10 min expiration).
2. Save a new task comment while assigning the author.
"""

from projects.repositories.task_comment_repository import CommentRepository
from django.core.cache import cache


class CommentService:
    """
    Service class for managing task comments.
    """

    @staticmethod
    def list_comments(user, task_id):
        """
        Retrieve comments for a specific task, using caching for optimization.

        Cache key format: `user_<user_id>_task_<task_id>_comments`

        Args:
            user (User): The currently authenticated user.
            task_id (int): The task ID whose comments are being retrieved.

        Returns:
            QuerySet: A queryset of TaskComment objects.
        """
        cache_key = f"user_{user.id}_task_{task_id}_comments"
        comments = cache.get(cache_key)

        if not comments:
            comments = CommentRepository.get_task_comments(task_id, user)
            cache.set(cache_key, comments, timeout=60 * 10)  # cache for 10 minutes

        return comments

    @staticmethod
    def create_comment(serializer, task_id, user):
        """
        Create a new comment on a task.

        Args:
            serializer (Serializer): DRF serializer with validated comment data.
            task_id (int): The task to which the comment belongs.
            user (User): The author of the comment.

        Returns:
            TaskComment: The newly created TaskComment object.
        """
        return serializer.save(task_id=task_id, author=user)
