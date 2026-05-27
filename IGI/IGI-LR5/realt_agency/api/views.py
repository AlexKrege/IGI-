from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .utils import get_multiple_rates, get_exchange_rates

class AsyncRatesView(View):
    async def get(self, request):
        rates = await get_multiple_rates(['USD', 'EUR', 'BYN'])
        return JsonResponse(rates, safe=False)

class SyncRatesView(View):
    @method_decorator(login_required)
    def get(self, request):
        data = get_exchange_rates('USD')
        return JsonResponse(data)