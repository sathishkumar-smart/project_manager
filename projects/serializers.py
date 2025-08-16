from rest_framework import serializers
from .models import Project,Task,TaskComment,ProjectMember,TaskAttachment
from django.contrib.auth import get_user_model

User= get_user_model()

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'updated_at']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
    queryset=User.objects.all(),
    required=False,
    allow_null=True)
    class Meta:
        model = Task
        read_only_fields=['created_by']
        fields = '__all__'

class TaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = '__all__'
        read_only_fields = ['author', 'created_at', 'updated_at']

class ProjectMemberSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = ProjectMember
        fields = ['id', 'project', 'user', 'user_email', 'role', 'joined_at']
        read_only_fields = ['project', 'joined_at']

class TaskAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAttachment
        fields = '__all__'
        read_only_fields = ['uploaded_at']