from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import TOKEN
from aiogram.enums import ParseMode
from database.db import initialize_db
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Инициализация бота
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties()
)

# Инициализация диспетчера
dp = Dispatcher()

# Инициализация базы данных
try:
    initialize_db()
    logger.info("База данных успешно инициализирована.")
except Exception as e:
    logger.error(f"Ошибка при инициализации базы данных: {e}")