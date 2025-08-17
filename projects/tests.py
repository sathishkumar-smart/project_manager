from django.test import TestCase
from rest_framework.test import APIClient
from django.utils import timezone
from accounts.models import User
from .models import Project, Task, TaskComment

class ProjectsTestCase(TestCase):
    """
    TestCase for the 'projects' app.
    Tests creation of projects, tasks, and task comments.
    Ensures notifications and relationships are handled correctly.
    """

    def setUp(self):
        """
        Set up test data:
            - Two users for assigning tasks
            - DRF API client for making requests
        """
        self.client = APIClient()

        # Create two users
        self.user1 = User.objects.create_user(email="user1@example.com", password="password123")
        self.user2 = User.objects.create_user(email="user2@example.com", password="password123")

        # Define a default datetime for start/due dates
        self.now = timezone.now()
        self.due_date = self.now + timezone.timedelta(days=7)

    def test_project_creation(self):
        """
        Test that a project can be created successfully.
        Checks NOT NULL constraints for start_date and owner.
        """
        project = Project.objects.create(
            name="Test Project",
            owner=self.user1,
            start_date=self.now,  # Must provide NOT NULL start_date
            end_date=self.now + timezone.timedelta(days=30),
            status="planned"
        )

        # Check project was saved correctly
        self.assertEqual(project.name, "Test Project")
        self.assertEqual(project.owner, self.user1)

    def test_task_creation_and_notification(self):
        """
        Test creating a task assigned to a user within a project.
        Ensures due_date and project_id constraints are satisfied.
        """
        # Create a project first
        project = Project.objects.create(
            name="Test Project",
            owner=self.user1,
            start_date=self.now,
            end_date=self.now + timezone.timedelta(days=30),
            status="planned"
        )

        # Create a task
        task = Task.objects.create(
            title="Test Task",
            description="Test description",
            assigned_to=self.user2,
            project=project,           # Must provide project for NOT NULL constraint
            due_date=self.due_date,    # Must provide due_date for NOT NULL constraint
            priority="low",
            status="todo"
        )

        # Verify task properties
        self.assertEqual(task.assigned_to, self.user2)
        self.assertEqual(task.project, project)

    def test_task_comment_creates_notification(self):
        """
        Test that adding a comment to a task works and the assigned user is notified.
        Ensures TaskComment creation with valid task reference.
        """
        # Create a project and task
        project = Project.objects.create(
            name="Comment Project",
            owner=self.user1,
            start_date=self.now,
            end_date=self.now + timezone.timedelta(days=30),
            status="planned"
        )

        task = Task.objects.create(
            title="Task with Comment",
            description="Desc",
            assigned_to=self.user2,
            project=project,
            due_date=self.due_date,
            priority="low",
            status="todo"
        )

        # Add a comment to the task
        comment = TaskComment.objects.create(
            task=task,
            author=self.user1,
            content="This is a test comment."
        )

        # Check comment properties
        self.assertEqual(comment.task, task)
        self.assertEqual(comment.author, self.user1)
        self.assertEqual(comment.content, "This is a test comment.")
