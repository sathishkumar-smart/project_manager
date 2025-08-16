"""
project_service.py

This service layer manages project-related operations.
It separates business logic from views and delegates database access
to the ProjectRepository.

Responsibilities:
1. Create a new project with the current user as the owner.
2. List all projects that belong to a given user.
3. Update an existing project.
"""

from projects.repositories.project_repository import ProjectRepository


class ProjectService:
    """
    Service class for handling business logic related to projects.
    """

    @staticmethod
    def create_project(serializer, user):
        """
        Create a new project.

        Args:
            serializer (Serializer): DRF serializer with validated project data.
            user (User): The user creating the project (owner).

        Returns:
            Project: The newly created Project instance.
        """
        return ProjectRepository.create_project(
            owner=user,
            **serializer.validated_data
        )

    @staticmethod
    def list_user_projects(user):
        """
        Get all projects owned by a user.

        Args:
            user (User): The user whose projects will be fetched.

        Returns:
            QuerySet: A queryset of Project objects.
        """
        return ProjectRepository.get_user_projects(user)

    @staticmethod
    def update_project(serializer, project):
        """
        Update an existing project.

        Args:
            serializer (Serializer): DRF serializer with validated data.
            project (Project): The project instance to update.

        Returns:
            Project: The updated Project instance.
        """
        return serializer.save()
