"""
member_service.py

This service layer manages project members.  
It ensures that views remain thin and delegates database logic to the repository.  

Responsibilities:
1. Fetch all members of a project.
2. Add a new member to a project.
3. Remove an existing member from a project.
"""

from projects.repositories.project_member_repository import MemberRepository


class MemberService:
    """
    Service class for managing project members.
    """

    @staticmethod
    def list_members(project_id):
        """
        Retrieve all members of a given project.

        Args:
            project_id (int): The ID of the project.

        Returns:
            QuerySet: A queryset of project member records.
        """
        return MemberRepository.get_project_members(project_id)

    @staticmethod
    def add_member(serializer, project_id):
        """
        Add a new member to a project.

        Args:
            serializer (Serializer): DRF serializer with validated member data.
            project_id (int): The project to which the member is being added.

        Returns:
            ProjectMember: The newly created ProjectMember object.
        """
        return serializer.save(project_id=project_id)

    @staticmethod
    def remove_member(member_id):
        """
        Remove a member from a project.

        Args:
            member_id (int): The ID of the member to remove.

        Returns:
            bool: True if removal was successful, False otherwise.
        """
        return MemberRepository.remove_member(member_id)
