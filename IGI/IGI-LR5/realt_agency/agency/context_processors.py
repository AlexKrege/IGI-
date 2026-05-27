from datetime import datetime
from django.utils import timezone as dj_timezone

def global_context(request):
    # Текущее время в UTC (без привязки к таймзоне)
    utc_now = datetime.utcnow()
    return {
        'utc_now': utc_now,
        'user_tz': getattr(request, 'user_timezone', None),
    }