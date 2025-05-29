from rest_framework.viewsets import ModelViewSet

from chats.models import Conversation, Message
from chats.serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filters = {
        'participants__username': ['exact', 'icontains'],
        'participants__email': ['exact', 'icontains'],
    }
    status = ''


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
