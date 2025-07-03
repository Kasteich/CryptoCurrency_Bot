import requests
import logging
from config import FIAT_API_URL, FIAT_API_KEY
from datetime import datetime, timedelta
from functools import lru_cache
import aiohttp


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fetch_query(url, params=None):
    """
    Универсальная функция для выполнения HTTP-запросов.
    :param url: URL для запроса
    :param params: Параметры запроса
    :return: Ответ от сервера в формате JSON или None (если ошибка)
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status() # Успешен ли запрос
                return await response.json()
    except aiohttp.ClientError as e:
        logger.error(f"Ошибка при выполнении запроса к {url}: {e}")
        return None


# Получение списка валют с Open Exchange Rates
@lru_cache(maxsize=32)
def get_currencies():
    try:
        response = requests.get(FIAT_API_URL, timeout=5)
        response.raise_for_status()
        return response.json().get('rates', {})
    except requests.RequestException as e:
        logger.error(f"Ошибка при запросе списка валют: {e}")
        return {}

# Получение цены для фиатных валют
async def get_fiat_price(symbol):
    url = f"https://openexchangerates.org/api/latest.json?app_id={FIAT_API_KEY}"
    data = await fetch_query(url)
    if data and 'rates' in data:
        return data['rates'].get(symbol.upper())
    return None


# Получение цены для криптовалют
async def get_crypto_price(symbol):
    crypto_name = get_crypto_name_by_symbol(symbol)
    if not crypto_name:
        return None

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': crypto_name,
        'vs_currencies': 'usd'
    }
    data = await fetch_query(url, params=params)
    if data and crypto_name in data:
        return data[crypto_name].get('usd')
    return None

# Получение истории цен криптовалют
async def get_crypto_price_history(symbol):
    crypto_name = get_crypto_name_by_symbol(symbol)
    if not crypto_name:
        return None

    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_name}/market_chart/range"
    params = {
        'vs_currency': 'usd',
        'from': int(start_date.timestamp()),
        'to': int(end_date.timestamp())
    }
    data = await fetch_query(url, params=params)
    if data and 'prices' in data:
        return [price[1] for price in data['prices']]
    return None

# Получение истории цен для фиатной валюты
async def get_fiat_price_history(symbol):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    history = []

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        url = f"https://openexchangerates.org/api/historical/{date_str}.json?app_id={FIAT_API_KEY}"
        data = await fetch_query(url)
        if data and 'rates' in data:
            rates = data['rates']
            if symbol.upper() in rates:
                history.append(rates[symbol.upper()])
        current_date += timedelta(days=1)

    if not history:
        logger.error(f"История цен для фиатной валюты {symbol} не найдена.")
        return None

    logger.info(f"История цен для фиатной валюты {symbol} загружена.")
    return history

async def fetch_rate(session, url, symbol):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            rates = data.get('rates', {})
            if symbol.upper() in rates:
                return rates[symbol.upper()]
    except Exception as e:
        logger.error(f"Ошибка при запросе {url}: {e}")
    return None

# Получение списка популярных криптовалют
async def get_popular_crypto_currencies():
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 20, # Ограничитель на 20 криптовалют
            'page': 1,
            'sparkline': False
        }
        data = await fetch_query(url, params=params)
        if data:
            return {crypto['name']: crypto['symbol'].upper() for crypto in data}
        return {}

# Получение точного имени криптовалюты по символу
def get_crypto_name_by_symbol(symbol):
    try:
        # Приоритетные символы и их имена
        priority_symbols = {
            'btc': 'bitcoin',
            'eth': 'ethereum',
            'usdt': 'tether',
            'bnb': 'binancecoin',
            'sol': 'solana',
            'xrp': 'ripple',
            'usdc': 'usd-coin',
            'ada': 'cardano',
            'avax': 'avalanche-2',
            'doge': 'dogecoin',
        }

        # Проверяем приоритетные символы
        if symbol.lower() in priority_symbols:
            return priority_symbols[symbol.lower()]

        # Если символ не в приоритетных, ищем в общем списке
        url = "https://api.coingecko.com/api/v3/coins/list"
        response = requests.get(url)
        response.raise_for_status()
        crypto_list = response.json()
        for crypto in crypto_list:
            if crypto['symbol'].lower() == symbol.lower():
                logger.info(f"Найдено имя криптовалюты для символа {symbol}: {crypto['id']}")
                return crypto['id']  # Возвращаем точное имя криптовалюты
        logger.error(f"Криптовалюта с символом {symbol} не найдена.")
        return None
    except requests.RequestException as e:
        logger.error(f"Ошибка при запросе списка криптовалют: {e}")
        return None

# Глобальный кэш для списка криптовалют
CRYPTO_LIST_CACHE = None

def get_crypto_list():
    global CRYPTO_LIST_CACHE
    if CRYPTO_LIST_CACHE is not None:
        return CRYPTO_LIST_CACHE

    try:
        url = "https://api.coingecko.com/api/v3/coins/list"
        response = requests.get(url)
        response.raise_for_status()
        CRYPTO_LIST_CACHE = response.json()
        return CRYPTO_LIST_CACHE
    except requests.RequestException as e:
        logger.error(f"Ошибка при запросе списка криптовалют: {e}")
        return None

# # Добавление задержки между запросами к API
# def get_crypto_price(symbol):
#     try:
#         # Получаем точное имя криптовалюты по символу
#         crypto_name = get_crypto_name_by_symbol(symbol)
#         if not crypto_name:
#             logger.error(f"Криптовалюта с символом {symbol} не найдена.")
#             return None
#
#         # Задержка для соблюдения лимита API
#         time.sleep(1)  # 1 секунда задержки
#
#         # Получаем цену криптовалюты
#         url = f"https://api.coingecko.com/api/v3/simple/price"
#         params = {
#             'ids': crypto_name,
#             'vs_currencies': 'usd'
#         }
#         response = requests.get(url, params=params)
#         response.raise_for_status()
#         logger.info(f"Ответ от CoinGecko для {symbol}: {response.json()}")
#         return response.json().get(crypto_name, {}).get('usd')
#     except requests.RequestException as e:
#         logger.error(f"Ошибка при запросе к CoinGecko: {e}")
#         return None

# Получение списка фиатных валют
@lru_cache(maxsize=32)
def get_fiat_currencies():
    try:
        response = requests.get(FIAT_API_URL)
        response.raise_for_status()
        return response.json().get('rates', {})
    except requests.RequestException:
        return {}


