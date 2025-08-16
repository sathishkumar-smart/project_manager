from django.test import TestCase
from django.contrib.auth import get_user_model
from projects.models import Project, Task

User = get_user_model()

class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@gmail.com',password="pass1234")

    def test_project_creation(self):
        project = Project.objects.create(name="Test Project", owner=self.user)
        self.assertEqual(project.name, "Test Project")
        self.assertEqual(project.owner, self.user)