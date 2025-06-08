from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from chats.filters import MessageFilter
from chats.models import Conversation, Message
from chats.pagination import MessagePagination
from chats.permissions import IsOwnerOrReadOnly
from chats.serializers import ConversationSerializer, MessageSerializer, ConversationViewSerializer, \
    ConversationViewWithMessageSerializer


class ConversationViewSet(ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filters = {
        'participants__username': ['exact', 'icontains'],
        'participants__email': ['exact', 'icontains'],
    }
    status = ''

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        if conversation_id:
            conversation = Conversation.objects.filter(id=conversation_id).first()
            if conversation and self.request.user in conversation.participants.all():
                return Message.objects.filter(conversation=conversation)
            else:
                return Response(
                    {"detail": "Forbidden: Not a participant of this conversation."},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            if self.request.user.is_authenticated:
                queryset = Conversation.objects.filter(participants=self.request.user)
                return queryset
        return Conversation.objects.none()

    def get_serializer_class(self):
        if self.action == 'list':
            conversation_id = self.kwargs.get('conversation_id')
            if conversation_id:
                return ConversationViewWithMessageSerializer
            return ConversationViewSerializer
        return super().get_serializer_class()


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(receiver_id=self.request.user.id)
