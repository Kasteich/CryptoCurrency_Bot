import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Токен для Telegram бота
TOKEN = os.getenv('TOKEN')

# API ключи для валют
CRYPTO_API_KEY = os.getenv('CRYPTO_API_KEY')
FIAT_API_KEY = os.getenv('FIAT_API_KEY')

# Имя базы данных
DB_NAME = os.getenv('DB_NAME')

# URL для API
CRYPTO_API_URL = 'https://api.coingecko.com/api/v3/'
FIAT_API_URL = f'https://openexchangerates.org/api/latest.json?app_id={FIAT_API_KEY}'

# Проверка загрузки
if not all([TOKEN, CRYPTO_API_KEY, FIAT_API_KEY, DB_NAME]):
    raise ValueError("Не все обязательные переменные окружения установлены")


