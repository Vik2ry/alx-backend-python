from datetime import datetime, time

from django.core.cache import cache
from rest_framework.exceptions import PermissionDenied


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else 'Anonymous'

        open(f"requests.log", 'a').write(
            f"{datetime.now().isoformat()} - User: {user}, Path: {request.path}\n"
        )

        response = self.get_response(request)

        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()

        start = time(18, 0)
        end = time(21, 0)

        if start <= now <= end:
            raise PermissionDenied('Access is restricted between 6 PM and 9 PM.')


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            ip = get_client_ip(request)

            cache_key = f"{ip}"

            count = cache.get(cache_key, 0)

            if count >= 5:
                raise PermissionDenied('Too many requests.')

            cache.set(cache_key, count + 1, timeout=3600)


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            user = request.user
            if not user.is_authenticated and not user.is_admin:
                raise PermissionDenied('You do not have permission to perform this action.')
        response = self.get_response(request)
        return response


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
