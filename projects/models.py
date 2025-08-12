from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User=get_user_model()

class Project(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField(blank=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE, related_name='projects')
    created_at=models.DateField(auto_now_add=True)

    class Meta:
        db_table="project"
        
    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES=[
        ('todo','To Do'),
        ('in_progress','In Progress'),
        ('done', 'Done'),
    ]

    title=models.CharField(max_length=200)
    description=models.TextField(blank=True)
    project=models.ForeignKey(Project, on_delete=models.CASCADE,related_name='tasks')
    assigned_to=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True,blank=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='todo')
    due_date=models.DateField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title