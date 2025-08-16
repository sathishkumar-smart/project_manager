"""
project_repository.py

Repository layer for managing Project persistence.
This layer is responsible for all database operations 
related to the Project model.

Responsibilities:
1. Create new projects.
2. Retrieve projects owned by a specific user.
3. Update existing project details.
"""

from projects.models import Project


class ProjectRepository:
    """
    Repository class for interacting with the Project model.
    Encapsulates all database queries and mutations related to projects.
    """

    @staticmethod
    def create_project(**kwargs):
        """
        Create a new project.

        Args:
            **kwargs: Fields required for creating a Project instance 
                      (e.g., `name`, `description`, `owner`, etc.).

        Returns:
            Project: The created Project instance.
        """
        return Project.objects.create(**kwargs)

    @staticmethod
    def get_user_projects(user):
        """
        Retrieve all projects owned by a specific user.

        Args:
            user (User): The user whose projects need to be fetched.

        Returns:
            QuerySet: A queryset of Project objects owned by the user.
        """
        return Project.objects.filter(owner=user)

    @staticmethod
    def update_project(project, **kwargs):
        """
        Update details of an existing project.

        Args:
            project (Project): The project instance to update.
            **kwargs: Fields and values to update on the project instance.

        Returns:
            Project: The updated Project instance.
        """
        for key, value in kwargs.items():
            setattr(project, key, value)
        project.save()
        return project
