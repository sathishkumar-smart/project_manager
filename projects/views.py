from rest_framework import viewsets, permissions,filters
from .models import Project,ProjectMember,Task,TaskComment
from .serializers import ProjectSerializer,TaskSerializer,TaskCommentSerializer,ProjectMemberSerializer
from .permissions import IsOwnerOrReadOnly,IsAssignedOrOwner,IsProjectMember
from django_filters.rest_framework import DjangoFilterBackend

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        ProjectMember.objects.create(project=project, user=self.request.user, role='owner')


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated,IsAssignedOrOwner,IsProjectMember]
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['priority', 'due_date', 'created_at']  # allowed ordering
    ordering = ['-priority']  # default ordering

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(assigned_to=self.request.user)

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
        serializer.save(
            task_id=self.kwargs['task_pk'],
            author=self.request.user
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