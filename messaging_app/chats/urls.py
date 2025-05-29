from django.urls import path, include
from rest_framework import routers

from chats.views import ConversationViewSet, MessageViewSet
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'message', MessageViewSet)

convo_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
convo_router.register(r'messages', MessageViewSet, basename='conversation-messages')
urlpatterns = [
    path('', include(router.urls)),
]
