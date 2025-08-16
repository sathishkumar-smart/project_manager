"""
serializers.py

This file contains Django REST Framework (DRF) serializers that convert
Django model instances into JSON for API responses, and validate/deserialize
incoming request data into Django model objects.

Serializers are directly tied to the models in `models.py`:
- Project
- Task
- TaskComment
- ProjectMember
- TaskAttachment
"""

from rest_framework import serializers
from .models import Project, Task, TaskComment, ProjectMember, TaskAttachment
from django.contrib.auth import get_user_model
from config.services.translation_service import TranslationService

# Use Django's custom User model (AUTH_USER_MODEL)
User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Project model.
    Used to create/update/list projects.
    - Owner is set automatically from request.user, so it's read-only.
    - Created/Updated timestamps are read-only fields.
    """

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'updated_at']


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    - assigned_to is optional and can be null.
    - created_by is set automatically in the view, so it's read-only.
    """

    # Allow assigning tasks to users by their ID (Primary Key)
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_by']


class TaskCommentSerializer(serializers.ModelSerializer):
    """
    Serializer for TaskComment model.
    - Adds translation support using TranslationService.
    - Provides both the original content and translated content.
    """

    # Overrides content to return a translated version
    content = serializers.SerializerMethodField()  
    translated_content = serializers.SerializerMethodField()  

    class Meta:
        model = TaskComment
        fields = '__all__'
        read_only_fields = ['author', 'created_at', 'updated_at']

    def get_content(self, obj):
        """Return translated comment content (default Hindi)."""
        translator = TranslationService()
        return translator.translate_text(obj.content, 'hi')

    def get_translated_content(self, obj):
        """Return translated content with explicit target language (Hindi)."""
        translator = TranslationService()
        return translator.translate_text(obj.content, target_language='hi')


class ProjectMemberSerializer(serializers.ModelSerializer):
    """
    Serializer for ProjectMember model.
    - Adds user_email field for convenience (read-only).
    - Project is auto-set from context, so it's read-only.
    """

    # Custom field to include user email
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = ProjectMember
        fields = ['id', 'project', 'user', 'user_email', 'role', 'joined_at']
        read_only_fields = ['project', 'joined_at']


class TaskAttachmentSerializer(serializers.ModelSerializer):
    """
    Serializer for TaskAttachment model.
    Used for uploading and fetching task-related attachments.
    - uploaded_at is read-only (auto-set by Django).
    """

    class Meta:
        model = TaskAttachment
        fields = '__all__'
        read_only_fields = ['uploaded_at']
