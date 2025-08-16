from rest_framework import viewsets, permissions,filters
from .models import Project,ProjectMember,Task,TaskComment,TaskAttachment
from notifications.models import Notification
from .serializers import ProjectSerializer,TaskSerializer,TaskCommentSerializer,ProjectMemberSerializer,TaskAttachmentSerializer
from .permissions import IsOwnerOrReadOnly,IsAssignedOrOwner,IsProjectMember
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied,APIException
from config.exceptions import InvalidTaskStatus
from config.utils.logger import custom_log

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        a=1/0
        ProjectMember.objects.create(project=project, user=self.request.user, role='owner')


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated,IsProjectMember]
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description','assigned_to__email', 'assigned_to__username']
    ordering_fields = ['priority', 'due_date', 'created_at']  # allowed ordering
    ordering = ['-priority']  # default ordering

    def perform_create(self, serializer):
        assigned_user = serializer.validated_data.get('assigned_to', None)
        if not assigned_user:
            assigned_user = self.request.user
        try:
            task=serializer.save(assigned_to=assigned_user,created_by=self.request.user)
            if task.assigned_to:
                Notification.objects.create(
                    recipient=task.assigned_to,
                    message=f"You have been assigned to task '{task.title}'"
                )
        except Exception as e:
            custom_log(f"Error: {str(e)}", file_path="task/comment/update.log", level="error")
            raise APIException("Failed to create task. Please try again.")
            
    def perform_update(self, serializer):
        assigned_to = self.request.data.get("assigned_to")
        status_value=self.request.get("status")
        if status_value not in ['todo','in_progress','completed']:
            raise InvalidTaskStatus()
        if assigned_to and not self.request.user.is_staff:
            raise PermissionDenied("You can't reassign tasks to others.")
        serializer.save()

class TaskCommentViewSet(viewsets.ModelViewSet):
    serializer_class = TaskCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter,IsProjectMember]
    search_fields = ['author__username', 'content']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return TaskComment.objects.filter(
            task_id=self.kwargs['task_pk'],
            task__project__owner=self.request.user
        )

    def perform_create(self, serializer):
        comment=serializer.save(
            task_id=self.kwargs['task_pk'],
            author=self.request.user
        )

        recipients = set()

        # Notify task owner
        if comment.task.created_by != self.request.user:
           recipients.add(comment.task.created_by)

        # Notify assignee
        if comment.task.assigned_to and comment.task.assigned_to != self.request.user:
            recipients.add(comment.task.assigned_to)

        for user in recipients:
            Notification.objects.create(
                recipient=user,
                message=f"New comment on task '{comment.task.title}'"
            )
            
class ProjectMemberViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_pk']
        return ProjectMember.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        serializer.save(project=project)

class TaskAttachmentViewSet(viewsets.ModelViewSet):
    queryset = TaskAttachment.objects.all()
    serializer_class = TaskAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskAttachment.objects.filter(task__project__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save()