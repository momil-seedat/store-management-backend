# notifications/views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer
from django.db.models import Count

class NotificationListCreateView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        # Automatically set the user_id to the current user when creating a notification
        serializer.save(user_id=self.request.user)
    def get_queryset(self):
        user_id = self.kwargs['user_id']  # Assuming 'user_id' is passed as a URL parameter
        return Notification.objects.filter(user_id=user_id)

    def list(self, request, *args, **kwargs):
        # Get the user_id from the URL parameters
        user_id = self.kwargs['user_id']

        # Filter notifications for the specified user_id
        queryset = self.get_queryset()

        # Count notifications with view_status=0
        view_notification_count = queryset.filter(view_status=False,user_id=user_id).count()

        # Serialize all notifications
        serializer = self.get_serializer(queryset, many=True)

        data = {
            'viewNotification': view_notification_count,
            'notifications': serializer.data
        }

        return Response(data)




class NotificationDetailView(generics.RetrieveAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
