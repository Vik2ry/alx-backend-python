from datetime import datetime, timedelta, time

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
