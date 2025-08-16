"""
urls.py

This file defines API routing for the project management app using DRF routers.
We use DefaultRouter and NestedDefaultRouter from `drf-nested-routers` to organize
endpoints for projects, tasks, comments, members, and attachments.

Endpoints:
- /projects/ → CRUD for projects
- /projects/{project_id}/members/ → Manage members in a project
- /tasks/ → CRUD for tasks
- /tasks/{task_id}/comments/ → Manage comments for a task
- /tasks/{task_id}/attachments/ → Manage file attachments for a task
"""

from django.urls import path, include
from rest_framework_nested import routers
from .views import (
    ProjectViewSet, TaskViewSet, TaskCommentViewSet,
    ProjectMemberViewSet, TaskAttachmentViewSet
)

# Base router for primary resources
router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')  
router.register(r'tasks', TaskViewSet, basename='task')          

# Nested router: tasks → comments
tasks_router = routers.NestedDefaultRouter(router, r'tasks', lookup='task')
tasks_router.register(r'comments', TaskCommentViewSet, basename='task-comments')

# Nested router: projects → members
projects_router = routers.NestedDefaultRouter(router, r'projects', lookup='project')
projects_router.register(r'members', ProjectMemberViewSet, basename='project-members')

# Nested router: tasks → attachments
tasks_router_attachment = routers.NestedDefaultRouter(router, r'tasks', lookup='task')
tasks_router_attachment.register(r'attachments', TaskAttachmentViewSet, basename='task-attachments')

# Combine all router URLs into urlpatterns
urlpatterns = [
    path('', include(router.urls)),                 
    path('', include(tasks_router.urls)),           
    path('', include(projects_router.urls)),        
    path('', include(tasks_router_attachment.urls)) 
]
