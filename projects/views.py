from rest_framework import generics,viewsets,permissions
from .models import Project,Task
from .serializers import ProjectSerializer,TaskSerializer

class ProjectViewSet(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    parser_classes=[permissions.IsAuthenticated]
    
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

