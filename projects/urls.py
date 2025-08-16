from django.urls import path, include
from rest_framework_nested import routers
from .views import ProjectViewSet, TaskViewSet, TaskCommentViewSet,ProjectMemberViewSet,TaskAttachmentViewSet

# Main router for projects and tasks
router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')

# Nested router: tasks → comments
tasks_router = routers.NestedDefaultRouter(router, r'tasks', lookup='task')
tasks_router.register(r'comments', TaskCommentViewSet, basename='task-comments')

projects_router = routers.NestedDefaultRouter(router, r'projects', lookup='project')
projects_router.register(r'members', ProjectMemberViewSet, basename='project-members')

tasks_router_attachment = routers.NestedDefaultRouter(router, r'tasks', lookup='task')
tasks_router_attachment.register(r'attachments', TaskAttachmentViewSet, basename='task-attachments')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(tasks_router.urls)),
    path('', include(projects_router.urls)),
    path('', include(tasks_router_attachment.urls))
]
