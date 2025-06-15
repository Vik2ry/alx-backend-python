from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.db import models

from messaging.models import Message
from messaging.serializers import MessageSerializer


class delete_user(APIView):
    def delete(self, request):
        user = request.user
        if not user:
            return Response({"error": "User not found."}, status=404)
        if not user.is_authenticated:
            return Response({"error": "User not authenticated."}, status=401)
        user.delete()
        return Response({"message": "User account deleted successfully."}, status=204)


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        request = self.request
        Message.objects.select_related('sender', 'receiver')
        queryset = Message.objects.filter(sender=request.user)
        return queryset.filter(receiver=request.user)


@cache_page(60)
@api_view(["GET"])
def unread_messages_view(request):
    user = request.user
    unread = Message.unread.unread_for_user(user)
    data = [{"id": m.id, "sender": m.sender.id, "content": m.content, "created_at": m.created_at} for m in unread]
    return Response(data)

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        return (
            super()
            .get_queryset()
            .filter(receiver=user, read=False)
            .only('id', 'sender', 'content', 'created_at')
        )