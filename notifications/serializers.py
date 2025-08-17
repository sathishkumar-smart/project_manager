from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model.
    Handles converting Notification instances to JSON and vice versa.
    """

    class Meta:
        model = Notification
        # Fields to be included in API responses
        fields = ['id', 'recipient', 'message', 'is_read', 'created_at']
        # Fields that should not be modified by API requests
        read_only_fields = ['recipient', 'created_at']

    def create(self, validated_data):
        """
        Automatically assign the recipient as the current user
        when creating a new notification (if context provides user).
        """
        user = self.context['request'].user if 'request' in self.context else None
        if user:
            validated_data['recipient'] = user
        return super().create(validated_data)
