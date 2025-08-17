# notifications/urls.py

from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet

# Create a router for notification endpoints
router = DefaultRouter()

# Register the NotificationViewSet with the router
# This automatically creates standard CRUD endpoints:
#   GET     /notifications/        -> list notifications
#   POST    /notifications/        -> create notification
#   GET     /notifications/{pk}/   -> retrieve a notification
#   PUT     /notifications/{pk}/   -> update a notification
#   PATCH   /notifications/{pk}/   -> partial update
#   DELETE  /notifications/{pk}/   -> delete a notification
router.register(r'notifications', NotificationViewSet, basename='notification')

# Include all router-generated URLs in urlpatterns
urlpatterns = router.urls
