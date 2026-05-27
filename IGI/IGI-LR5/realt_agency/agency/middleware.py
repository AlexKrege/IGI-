import pytz
from django.utils import timezone
from api.utils import get_user_timezone

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        tz_name = get_user_timezone(ip)
        if tz_name:
            request.user_timezone = pytz.timezone(tz_name)
            timezone.activate(request.user_timezone)
        else:
            # По умолчанию – Минск
            default_tz = pytz.timezone('Europe/Minsk')
            request.user_timezone = default_tz
            timezone.activate(default_tz)
        response = self.get_response(request)
        return response