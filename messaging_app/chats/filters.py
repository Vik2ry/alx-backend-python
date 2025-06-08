import django_filters
from chats.models import Message


class MessageFilter(django_filters.FilterSet):

    user = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    sent_between = django_filters.DateTimeFromToRangeFilter(field_name='sent_at')

    class Meta:
        model = Message
        fields = ['conversation', 'user']
