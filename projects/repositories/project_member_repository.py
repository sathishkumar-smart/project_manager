"""
member_repository.py

Repository layer for managing ProjectMember persistence.
This layer is responsible for all database interactions 
related to project memberships.

Responsibilities:
1. Add members to a project.
2. Fetch members belonging to a project.
3. Remove members from a project.
"""

from projects.models import ProjectMember


class MemberRepository:
    """
    Repository class for interacting with the ProjectMember model.
    Encapsulates all database queries related to project memberships.
    """

    @staticmethod
    def add_member(**kwargs):
        """
        Add a new member to a project.

        Args:
            **kwargs: Fields required for creating a ProjectMember.
                      Typically includes `project_id` and `user`.

        Returns:
            ProjectMember: The created ProjectMember instance.
        """
        return ProjectMember.objects.create(**kwargs)

    @staticmethod
    def get_project_members(project_id):
        """
        Retrieve all members of a given project.

        Args:
            project_id (int): The ID of the project.

        Returns:
            QuerySet: A queryset of ProjectMember objects.
        """
        return ProjectMember.objects.filter(project_id=project_id)

    @staticmethod
    def remove_member(member_id):
        """
        Remove a member from a project.

        Args:
            member_id (int): The ID of the ProjectMember record to delete.

        Returns:
            tuple: (number of deleted objects, {deleted object details}).
        """
        return ProjectMember.objects.filter(id=member_id).delete()
