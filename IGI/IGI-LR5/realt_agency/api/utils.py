import requests
import aiohttp  
import asyncio

def get_exchange_rates(base='USD'):
    url = f'https://api.exchangerate.host/latest?base={base}'
    try:
        resp = requests.get(url, timeout=3)
        if resp.ok:
            return resp.json()
    except:
        pass
    return {}

async def fetch_currency(session, base):
    url = f'https://api.exchangerate.host/latest?base={base}'
    async with session.get(url) as resp:
        return await resp.json()

async def get_multiple_rates(bases=['USD', 'EUR']):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_currency(session, base) for base in bases]
        return await asyncio.gather(*tasks)

def get_user_timezone(ip):
    if ip.startswith('127.') or ip == 'localhost':
        return 'Europe/Minsk'
    url = f'https://ipapi.co/{ip}/json/'
    try:
        resp = requests.get(url, timeout=2)
        if resp.ok:
            data = resp.json()
            return data.get('timezone', 'UTC')
    except:
        pass
    return 'UTC'

# def get_usd_rate():
#     import requests
#     url = "https://api.exchangerate.host/latest?base=USD&symbols=BYN"
#     try:
#         resp = requests.get(url, timeout=3)
#         if resp.ok:
#             data = resp.json()
#             return float(data['rates']['BYN'])
#     except:
#         pass
#     return None  # Если API недоступен

def get_usd_rate():
    """
    Курс USD/BYN от Национального банка Беларуси (официальный курс)
    """
    url = "https://api.nbrb.by/exrates/rates/145?parammode=2"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # В ответе: {"Cur_ID":145,"Date":"2025-05-27","Cur_OfficialRate":3.2}
            return float(data['Cur_OfficialRate'])
    except Exception as e:
        print(f"Ошибка получения курса: {e}")
    # fallback
    return 3.2