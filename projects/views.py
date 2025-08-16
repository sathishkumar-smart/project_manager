"""
views.py

This module defines DRF ViewSets for handling project management operations.
Each ViewSet is responsible only for request/response handling and delegates
the core business logic to the corresponding service layer (ProjectService,
TaskService, etc.), ensuring a clean separation of concerns.

ViewSets included:
- ProjectViewSet        : CRUD operations for projects.
- TaskViewSet           : CRUD operations for tasks within projects.
- TaskCommentViewSet    : Managing comments on tasks.
- ProjectMemberViewSet  : Managing project members.
- TaskAttachmentViewSet : Managing file attachments for tasks.
"""

from rest_framework import viewsets, permissions, filters
from .serializers import (
    ProjectSerializer, TaskSerializer, TaskCommentSerializer,
    ProjectMemberSerializer, TaskAttachmentSerializer
)
from .permissions import IsProjectMember

# Services (business logic layer)
from .services.project_service import ProjectService
from .services.task_service import TaskService
from .services.attachment_service import AttachmentService
from .services.member_service import MemberService
from .services.comment_service import CommentService


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing projects.

    Features:
        - Authenticated users only.
        - Supports listing, creating, updating, and deleting projects.
        - Delegates logic to `ProjectService`.

    Endpoints:
        - GET    /projects/           → List user’s projects
        - POST   /projects/           → Create a new project
        - GET    /projects/{id}/      → Retrieve a project
        - PUT    /projects/{id}/      → Update an existing project
        - DELETE /projects/{id}/      → Delete a project
    """

    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Fetch projects belonging to the authenticated user.

        Returns:
            QuerySet: List of `Project` instances owned by the current user.
        """
        return ProjectService.list_user_projects(self.request.user)

    def perform_create(self, serializer):
        """
        Create a new project using ProjectService.

        Args:
            serializer (ProjectSerializer): Validated project data.
        """
        ProjectService.create_project(serializer, self.request.user)

    def perform_update(self, serializer):
        """
        Update an existing project using ProjectService.

        Args:
            serializer (ProjectSerializer): Validated project data with updates.
        """
        ProjectService.update_project(serializer, serializer.instance)


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing tasks within projects.

    Features:
        - Restricted to authenticated users who are project members.
        - Supports filtering, searching, and ordering.
        - Delegates logic to `TaskService`.

    Endpoints:
        - GET    /projects/{project_id}/tasks/         → List tasks
        - POST   /projects/{project_id}/tasks/         → Create a new task
        - GET    /projects/{project_id}/tasks/{id}/    → Retrieve a task
        - PUT    /projects/{project_id}/tasks/{id}/    → Update a task
        - DELETE /projects/{project_id}/tasks/{id}/    → Delete a task
    """

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectMember]
    queryset = TaskService  # Service handles actual queries

    # Enable filtering, searching, and ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description", "assigned_to__email", "assigned_to__username"]
    ordering_fields = ["priority", "due_date", "created_at"]
    ordering = ["-priority"]

    def perform_create(self, serializer):
        """
        Create a new task using TaskService.

        Args:
            serializer (TaskSerializer): Validated task data.
        """
        TaskService.create_task(serializer, self.request)

    def perform_update(self, serializer):
        """
        Update an existing task using TaskService.

        Args:
            serializer (TaskSerializer): Validated task data with updates.
        """
        TaskService.update_task(serializer, self.request)


class TaskCommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing comments on tasks.

    Features:
        - Only authenticated users can create and view comments.
        - Delegates logic to `CommentService`.

    Endpoints:
        - GET    /tasks/{task_id}/comments/        → List comments for a task
        - POST   /tasks/{task_id}/comments/        → Add a comment
        - GET    /tasks/{task_id}/comments/{id}/   → Retrieve a comment
        - PUT    /tasks/{task_id}/comments/{id}/   → Update a comment
        - DELETE /tasks/{task_id}/comments/{id}/   → Delete a comment
    """

    serializer_class = TaskCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Fetch comments for a given task.

        Args:
            task_pk (int): Task ID from URL.

        Returns:
            QuerySet: List of `TaskComment` instances.
        """
        return CommentService.list_comments(self.request.user, self.kwargs["task_pk"])

    def perform_create(self, serializer):
        """
        Create a new comment using CommentService.

        Args:
            serializer (TaskCommentSerializer): Validated comment data.
        """
        CommentService.create_comment(serializer, self.kwargs["task_pk"], self.request.user)


class ProjectMemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing project members.

    Features:
        - Authenticated users only.
        - Allows adding/listing members of a project.
        - Delegates logic to `MemberService`.

    Endpoints:
        - GET    /projects/{project_id}/members/        → List project members
        - POST   /projects/{project_id}/members/        → Add a member
        - GET    /projects/{project_id}/members/{id}/   → Retrieve a member
        - PUT    /projects/{project_id}/members/{id}/   → Update a member
        - DELETE /projects/{project_id}/members/{id}/   → Remove a member
    """

    serializer_class = ProjectMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Fetch members for a given project.

        Args:
            project_pk (int): Project ID from URL.

        Returns:
            QuerySet: List of `ProjectMember` instances.
        """
        return MemberService.list_members(self.kwargs["project_pk"])

    def perform_create(self, serializer):
        """
        Add a new member to a project using MemberService.

        Args:
            serializer (ProjectMemberSerializer): Validated member data.
        """
        MemberService.add_member(serializer, self.kwargs["project_pk"])


class TaskAttachmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing task attachments.

    Features:
        - Handles file uploads and retrieval of attachments.
        - Authenticated users only.
        - Delegates logic to `AttachmentService`.

    Endpoints:
        - GET    /tasks/{task_id}/attachments/        → List attachments for a task
        - POST   /tasks/{task_id}/attachments/        → Upload a new attachment
        - GET    /tasks/{task_id}/attachments/{id}/   → Retrieve an attachment
        - PUT    /tasks/{task_id}/attachments/{id}/   → Update an attachment
        - DELETE /tasks/{task_id}/attachments/{id}/   → Delete an attachment
    """

    serializer_class = TaskAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Fetch attachments for a given task.

        Args:
            task_pk (int): Task ID from URL.

        Returns:
            QuerySet: List of `TaskAttachment` instances.
        """
        return AttachmentService.list_attachments(self.request.user, self.kwargs["task_pk"])

    def perform_create(self, serializer):
        """
        Create a new attachment using AttachmentService.

        Args:
            serializer (TaskAttachmentSerializer): Validated attachment data.
        """
        AttachmentService.create_attachment(serializer, self.kwargs["task_pk"], self.request.user)
