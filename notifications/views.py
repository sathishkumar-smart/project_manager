# notifications/views.py

from rest_framework import viewsets, permissions, decorators, response
from .serializers import NotificationSerializer
from services.notification_service import NotificationService

class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing notifications.
    All business logic is handled by NotificationService.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return notifications for the current authenticated user.
        """
        return NotificationService.list_user_notifications(self.request.user)

    def perform_create(self, serializer):
        """
        Create a notification for the current user.
        """
        NotificationService.create_user_notification(
            user=self.request.user,
            message=serializer.validated_data['message']
        )

    @decorators.action(detail=True, methods=['patch'])
    def mark_as_read(self, request, pk=None):
        """
        Mark a notification as read using the service layer.
        """
        notification = self.get_object()
        NotificationService.mark_notification_as_read(notification)
        return response.Response({'status': 'marked as read'})
