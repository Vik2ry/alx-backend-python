from django.urls import path

from messaging.views import delete_user

urlpatterns = [
    path('user/', delete_user.as_view(), name='user-api'),
]