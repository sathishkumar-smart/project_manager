from django.db import models
from django.conf import settings


class Project(models.Model):
    """
    Represents a project entity that groups related tasks and members.

    Attributes:
        name (str): Name of the project.
        description (str): Optional text description of the project.
        owner (User): The user who owns the project.
        start_date (date): Project start date.
        end_date (date): Optional project end date.
        status (str): Current status of the project (planned, in_progress, completed, on_hold).
        created_at (datetime): Auto-generated timestamp when the project is created.
        updated_at (datetime): Auto-updated timestamp when the project is modified.
    """

    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )  # If user is deleted, their projects are deleted too
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation: project name."""
        return self.name


class Task(models.Model):
    """
    Represents a task under a project.

    Attributes:
        project (Project): The project this task belongs to.
        title (str): Short task title.
        description (str): Detailed description of the task.
        status (str): Current task status (todo, in_progress, completed).
        priority (str): Task priority (low, medium, high).
        assigned_to (User): The user assigned to complete the task.
        due_date (date): Deadline for the task.
        created_by (User): The user who created the task.
        created_at (datetime): Auto-generated timestamp when created.
        updated_at (datetime): Auto-updated timestamp when modified.
    """

    STATUS_CHOICES = [
        ('todo', 'ToDo'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='parent_project'
    )  # Deleting a project deletes its tasks
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='low')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks"
    )  # Task can remain unassigned if user is removed
    due_date = models.DateField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name='created_tasks'
    )  # Track who created the task
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation: task title + project name."""
        return f"{self.title} ({self.project.name})"


class TaskComment(models.Model):
    """
    Represents comments left on a specific task.

    Attributes:
        task (Task): The related task.
        author (User): User who wrote the comment.
        content (str): The comment text.
        created_at (datetime): Auto-generated timestamp when created.
        updated_at (datetime): Auto-updated timestamp when modified.
        is_deleted (bool): Soft-delete flag for hiding comments without removing them.
    """

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='task_comments'
    )
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)  # Soft delete instead of permanent deletion

    def __str__(self):
        """String representation: comment author and task."""
        return f"Comment by {self.author} on {self.task}"


class ProjectMember(models.Model):
    """
    Represents a user’s membership in a project with a defined role.

    Attributes:
        project (Project): The project joined.
        user (User): The member user.
        role (str): Member role (owner, member, viewer).
        joined_at (datetime): Timestamp when the user joined.
    """

    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('member', 'Member'),
        ('viewer', 'Viewer'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="project_memberships")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'user')  # Prevent duplicate memberships

    def __str__(self):
        """String representation: user’s role in project."""
        return f"{self.user} in {self.project} as {self.role}"


class TaskAttachment(models.Model):
    """
    Represents a file attachment for a task.

    Attributes:
        task (Task): The related task.
        file (File): The uploaded file (stored in MEDIA_ROOT/tasks/).
        uploaded_at (datetime): Timestamp when file was uploaded.
    """

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='tasks/')  # Stored in MEDIA_ROOT/tasks/
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation: filename + task title."""
        return f"{self.file.name} for {self.task.title}"
